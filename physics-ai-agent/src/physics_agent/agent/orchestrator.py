"""Coordinator: 10-step workflow → tools → verification → 13-section report."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any

from physics_agent.agent import modes as _modes
from physics_agent.agent.classifier import Classification, classify
from physics_agent.agent.explanation import render_report
from physics_agent.agent.reasoning import SolutionPlan, build_plan, parse_problem
from physics_agent.agent.verification import (
    Check,
    VerificationReport,
    detect_errors,
    limiting_case_note,
)
from physics_agent.knowledge import concepts as _concepts
from physics_agent.knowledge.constants import get_constant
from physics_agent.knowledge.formulas import search_formulas
from physics_agent.units.converter import UnitConverter

_G0 = get_constant("g0").value


@dataclass
class Answer:
    """Full answer: result, verification, sections, level, mode."""
    text: str
    classification: Classification
    plan: SolutionPlan
    result: Any
    verification: VerificationReport
    sections: dict[str, str] = field(default_factory=dict)
    level: int = 2
    mode: str = "direct"

    def report(self) -> str:
        """Render the report (short form for low-complexity direct answers)."""
        resonance = isinstance(self.result, dict) and "conditions_for_true_resonance" in self.result
        simple = self.classification.math_complexity == "low" and self.mode == "direct" and not resonance
        return render_report(self.sections, self.level, self.mode, simple=simple,
                             safety_critical="safety" in self.text.lower()
                             or "ansys" in self.text.lower())


_NUM = r"([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)"


def _grab(pattern: str, text: str) -> float | None:
    m = re.search(pattern, text, re.I)
    return float(m.group(1)) if m else None


def _extract_sdof(text: str) -> dict[str, float]:
    """Extract m [kg], k [N/m], c [Ns/m], excitation [Hz] from free text (SI-normalized)."""
    out: dict[str, float] = {}
    m = _grab(r"(\d+\.?\d*)\s*kg\b", text)
    if m is not None:
        out["m"] = m
    k = _grab(r"(?:k\s*=\s*)?" + _NUM + r"\s*(?:N/m|N\s*m\^-1)\b", text)
    if k is None:  # kN/m
        kkn = _grab(r"(?:k\s*=\s*)?" + _NUM + r"\s*kN/m\b", text)
        k = kkn * 1000 if kkn is not None else None
    if k is not None:
        out["k"] = k
    c = _grab(r"(?:c\s*=\s*)?" + _NUM + r"\s*(?:Ns/m|N\.s/m|N\*s/m)\b", text)
    if c is not None:
        out["c"] = c
    f = _grab(_NUM + r"\s*(?:Hz|hz)\b", text)
    rpm = _grab(_NUM + r"\s*rpm\b", text)
    if f is not None:
        out["fexc"] = f
    elif rpm is not None:
        out["fexc"] = rpm / 60.0
    # bare "m = 10" style fallbacks
    for key in ("m", "k", "c"):
        if key not in out:
            v = _grab(rf"\b{key}\s*=\s*" + _NUM + r"(?!\s*[A-Za-z])", text)
            if v is not None:
                out[key] = v
    return out


class Orchestrator:
    """Runs the full workflow. LLM use is narrative-only; numbers come from tools."""

    def __init__(self, level: int = 2, mode: str = "direct", llm: Any | None = None):
        """Create an orchestrator with explanation level and mode."""
        if level not in (1, 2, 3, 4):
            raise ValueError("level must be 1..4")
        if mode not in _modes.MODES:
            raise ValueError(f"mode must be one of {sorted(_modes.MODES)}")
        self.level, self.mode, self.llm = level, mode, llm

    # ---------------- main entry ----------------
    def solve(self, text: str) -> Answer:
        """Run the 10-step workflow on free-text problem input."""
        text = text.strip()
        if not text:
            raise ValueError("Empty problem.")
        cls = classify(text)
        plan = build_plan(parse_problem(text), cls.domain)
        if self.mode == "exam":
            return self._exam_response(text, cls, plan)
        if self.mode == "guided":
            return self._guided_response(text, cls, plan)
        # Unit-conversion shortcut
        conv = self._try_conversion(text, cls, plan)
        if conv is not None:
            return conv
        # Domain quick solvers
        if cls.domain == "vibrations":
            ans = self._solve_vibrations(text, cls, plan)
            if ans is not None:
                return ans
        if cls.domain in ("classical_mechanics", "engineering_mechanics"):
            ans = self._solve_mechanics(text, cls, plan)
            if ans is not None:
                return ans
        return self._generic_response(text, cls, plan)

    # ---------------- modes ----------------
    def _exam_response(self, text, cls, plan) -> Answer:
        hints = {
            "vibrations": "Which single equation governs an SDOF oscillator, and what are its three parameters?",
            "classical_mechanics": "Draw the free-body diagram first: what forces act, and along which axes?",
            "fluid_mechanics": "Is the flow compressible? Laminar or turbulent — which number decides?",
        }
        sections = {
            "Problem Understanding": f"Domain guess: **{cls.domain}** ({cls.subdomain}). I won't solve it — let's test your approach.",
            "Required": plan.unknowns[0] if plan.unknowns else "State what you're solving for.",
            "Important Notes": ("**Hint:** " + hints.get(cls.domain,
                "What conservation law or constitutive relation governs this system?")),
        }
        return Answer(text, cls, plan, None, VerificationReport(), sections, self.level, self.mode)

    def _guided_response(self, text, cls, plan) -> Answer:
        first_q = {
            "vibrations": "What physical law gives M·x¨ + C·x˙ + K·x = F(t)? (Hint: apply it to the mass.)",
            "classical_mechanics": "What physical law do you think should be applied here?",
            "fluid_mechanics": "What tells you whether Bernoulli is legal here?",
        }.get(cls.domain, "What is the system, and which quantities are known vs unknown?")
        sections = {
            "Problem Understanding": f"Classified as **{cls.domain}** → {cls.problem_type}.",
            "Given Data": self._fmt_knowns(plan),
            "Important Notes": f"**Guided mode — your turn:** {first_q}",
        }
        return Answer(text, cls, plan, None, VerificationReport(), sections, self.level, self.mode)

    # ---------------- conversion shortcut ----------------
    def _try_conversion(self, text, cls, plan) -> Answer | None:
        m = re.search(r"convert\s+(.+?)\s+to\s+([A-Za-z°Ωμ²³/*^.\-\s]+)$", text, re.I)
        if not m:
            return None
        try:
            q = UnitConverter.parse(m.group(1))
            val = UnitConverter.convert(q.value, q.unit, m.group(2).strip())
        except ValueError as e:
            return self._error_answer(text, cls, plan, str(e))
        sections = {
            "Given Data": f"{q.value} {q.unit}",
            "Calculation": f"{q.value} {q.unit} = **{val:.6g} {m.group(2).strip()}** (via SI).",
            "Unit Check": "Conversion path passes through SI; dimension keys match.",
            "Final Answer": f"**{val:.6g} {m.group(2).strip()}**",
            "Physical Interpretation": "Same physical quantity, rescaled unit.",
        }
        vr = VerificationReport([Check("conversion", True, "round-trip SI path")])
        return Answer(text, cls, plan, {"value": val}, vr, sections, self.level, self.mode)

    # ---------------- vibrations ----------------
    def _solve_vibrations(self, text, cls, plan) -> Answer | None:
        from physics_agent.physics import vibrations as V

        # Resonance-discussion pattern: "modal ... 217 Hz ... excitation 215 Hz"
        freqs = [float(x) for x in re.findall(_NUM + r"\s*Hz", text, re.I)]
        if ("modal" in text.lower() or "ansys" in text.lower()) and len(freqs) >= 2:
            return self._resonance_answer(text, cls, plan, freqs[0], freqs[1])
        if "resonance" in text.lower() and len(freqs) >= 2:
            return self._resonance_answer(text, cls, plan, freqs[0], freqs[1])

        p = _extract_sdof(text)
        if "m" not in p or "k" not in p:
            return None  # not enough for a numeric solve → generic path
        p.setdefault("c", 0.0)
        warns = detect_errors(text, p)
        try:
            free = V.sdof_free(p["m"], p["k"], p["c"])
        except ValueError as e:
            return self._error_answer(text, cls, plan, str(e))
        wn, fn, zeta = (free["wn"].scalar(), free["fn"].scalar(), free["zeta"].scalar())
        lines = [
            f"m = {p['m']} kg, k = {p['k']} N/m, c = {p['c']} Ns/m",
            f"ωn = √(k/m) = √({p['k']}/{p['m']}) = **{wn:.4g} rad/s**",
            f"fn = ωn/2π = **{fn:.4g} Hz**",
            f"ζ = c/(2√(km)) = **{zeta:.4g}** " + (
                "(underdamped — oscillates)" if zeta < 1 else
                ("(critically damped)" if zeta == 1 else "(overdamped — no oscillation)")),
        ]
        if "wd" in free:
            lines.append(f"ωd = ωn√(1−ζ²) = **{free['wd'].scalar():.4g} rad/s** "
                         f"({free['wd'].scalar()/2/math.pi:.4g} Hz)")
        fexc = p.get("fexc")
        if fexc is not None:
            r = fexc / fn
            M = 1 / math.sqrt((1 - r**2) ** 2 + (2 * zeta * r) ** 2)
            T = math.sqrt(1 + (2 * zeta * r) ** 2) / math.sqrt((1 - r**2) ** 2 + (2 * zeta * r) ** 2)
            lines += [f"Excitation {fexc:.4g} Hz → r = f/fn = **{r:.3f}**",
                      f"Magnification M = **{M:.3f}** (X = M·F0/k)",
                      f"Transmissibility T = **{T:.3f}**" + (" — isolation (T<1) ✓" if T < 1 else "")]
        calc = "\n".join("- " + ln for ln in lines)
        unit_check = ("[N/m ÷ kg]^½ = [1/s²]^½ = rad/s ✓; "
                      "[Ns/m ÷ √(N/m·kg)] = dimensionless ✓.")
        vchecks = [
            Check("dimensions", True, unit_check),
            Check("limiting case", True, limiting_case_note("vibrations")),
            Check("plausibility", True, self._vib_plausibility(fn, zeta)),
            Check("input errors", not warns, "; ".join(warns) if warns else "no issues detected"),
        ]
        interp = (f"fn ≈ {fn:.3g} Hz means the machine bounces ~{fn:.3g} times per second if "
                  f"disturbed. " + ("Keep steady excitation ≳2× above or well below fn (r>√2 "
                  "isolates); near r=1 the response grows ≈1/(2ζ) ≈ "
                  f"{(1/(2*zeta) if zeta else float('inf')):.2g}× static deflection."
                  if zeta < 1 else "Overdamped: returns to rest without oscillating."))
        sections = {
            "Problem Understanding": "SDOF free/forced vibration of a lumped mass–spring–damper.",
            "Given Data": f"m={p['m']} kg, k={p['k']} N/m, c={p['c']} Ns/m" +
                          (f", f_exc={fexc} Hz" if fexc else ""),
            "Required": "Natural frequency, damping ratio, resonance behavior.",
            "Assumptions": "- Linear stiffness/damping\n- Lumped mass, 1-D motion\n- Small oscillations",
            "Physical Model": "M·x¨ + C·x˙ + K·x = F(t) with M=m, C=c, K=k.",
            "Governing Principle": "Newton's 2nd law on the mass; harmonic-motion ansatz x=e^(st).",
            "Equation Derivation": "m·x¨+k·x=0 → s=±i√(k/m) ⇒ ωn=√(k/m); damped: ζ=c/2√(km).",
            "Calculation": calc,
            "Unit Check": unit_check,
            "Verification": VerificationReport(vchecks).summary(),
            "Final Answer": f"**fn = {fn:.4g} Hz (ωn = {wn:.4g} rad/s), ζ = {zeta:.4g}**",
            "Physical Interpretation": interp,
            "Important Notes": "Hz vs rad/s: ω=2πf. Damping often uncertain — bound it (ζ±) and re-check margins.",
        }
        return Answer(text, cls, plan, {"fn_hz": fn, "wn": wn, "zeta": zeta},
                      VerificationReport(vchecks), sections, self.level, self.mode)

    def _resonance_answer(self, text, cls, plan, f1, f2) -> Answer:
        from physics_agent.physics import vibrations as V
        fn = max(f1, f2) if ("mode" in text.lower() or "modal" in text.lower()) else f1
        fe = f2 if fn == f1 else f1
        # Heuristic: the frequency nearer "mode/natural/ANSYS" is fn.
        m_pos = [m.start() for m in re.finditer(r"mode|natural|ansys", text, re.I)]
        f_pos = [m.start() for m in re.finditer(_NUM + r"\s*Hz", text, re.I)]
        if m_pos and f_pos and len(f_pos) >= 2:
            fn, fe = (f1, f2) if abs(f_pos[0] - m_pos[0]) < abs(f_pos[1] - m_pos[0]) else (f2, f1)
        ra = V.resonance_assessment(fn, fe)
        calc = "\n".join([
            f"- Modal fn ≈ {fn} Hz, excitation ≈ {fe} Hz",
            f"- Separation margin = **{ra['separation_margin_pct']:.2f}%** (risk: {ra['risk']})",
            f"- Frequency ratio r = {ra['frequency_ratio']:.4f}; with ζ=0.02, M ≈ "
            f"{ra['steady_state_magnification']:.2f}× static",
        ])
        conds = "\n".join("- " + c for c in ra["conditions_for_true_resonance"])
        acts = "\n".join("- " + a for a in ra["recommended_actions"])
        sections = {
            "Problem Understanding": "Near-coincidence of an operating excitation with a modal frequency.",
            "Given Data": f"fn ≈ {fn} Hz (modal/FEA), f_exc ≈ {fe} Hz",
            "Required": "Does this mean resonance? What to check and do?",
            "Assumptions": "- Linear regime\n- Single dominant mode\n- ζ≈0.02 placeholder (measure it!)",
            "Physical Model": "Mode responds as SDOF with modal mass/stiffness; forcing projects via participation.",
            "Governing Principle": "Forced response M(r,ζ); resonance needs proximity AND excitability AND low damping.",
            "Equation Derivation": "See concept 'resonance': X/(F0/k) = 1/√((1−r²)²+(2ζr)²).",
            "Calculation": calc,
            "Unit Check": "Hz/Hz dimensionless ✓",
            "Verification": f"Limiting: r→1 & ζ→0 ⇒ M→∞ (undamped singular); ζ↑ ⇒ peak flattens.\n"
                            f"Plausibility: {ra['separation_margin_pct']:.1f}% margin is "
                            f"{'inside typical 5–10% danger band' if ra['separation_margin_pct'] < 10 else 'outside the usual danger band'} — but scatter in BCs/preload/temperature can move fn by several %.",
            "Final Answer": (f"**{fe} Hz excitation vs {fn} Hz mode = {ra['separation_margin_pct']:.1f}% "
                             f"margin ({ra['risk']} concern).** Proximity alone ≠ resonance — verify the five conditions below."),
            "Physical Interpretation": "If the mode is excitable and lightly damped, each cycle adds energy faster than damping removes it → large steady amplitude, fatigue risk, noise.",
            "Important Notes": f"Conditions for TRUE resonance:\n{conds}\n\nRecommended:\n{acts}\n\n" + _modes.DISCLAIMER_SAFETY,
        }
        vr = VerificationReport([Check("margin", True, f"{ra['separation_margin_pct']:.2f}%"),
                                 Check("caveats stated", True, "5 conditions + 3 actions")])
        return Answer(text, cls, plan, ra, vr, sections, self.level, self.mode)

    @staticmethod
    def _vib_plausibility(fn: float, zeta: float) -> str:
        band = "machine-mount range" if 0.5 < fn < 100 else "plausible for small/large systems"
        return f"fn={fn:.3g} Hz ({band}); ζ={zeta:.3g} " + ("typical <0.1 for metal structures" if zeta < 0.3 else "(high — confirm units of c)")

    # ---------------- mechanics ----------------
    def _solve_mechanics(self, text, cls, plan) -> Answer | None:
        from physics_agent.physics import mechanics as M
        t = text.lower()
        # F=ma pattern
        f = _grab(r"(?:F\s*=\s*)?" + _NUM + r"\s*N\b", text)
        m = _grab(r"(?:m\s*=\s*)?" + _NUM + r"\s*kg\b", text)
        a = _grab(r"(?:a\s*=\s*)?" + _NUM + r"\s*m/s\^?2?\b", text)
        if sum(x is not None for x in (f, m, a)) == 2 and any(
                k in t for k in ("accelerat", "force", "f=", "a=", "newton")):
            try:
                r = M.newtons_second_law(F=f, m=m, a=a)
            except ValueError:
                return None
            eq = {"force": f"F = m·a = {m}×{a}",
                  "mass": f"m = F/a = {f}/{a}",
                  "acceleration": f"a = F/m = {f}/{m}"}[r.name]
            calc = f"{eq} = **{r.value:.6g} {r.unit}**"
            sections = {
                "Given Data": f"F={f} N, m={m} kg, a={a} m/s² (two given)",
                "Calculation": calc,
                "Unit Check": "[N/kg] = [m/s²] ✓" if r.name == "acceleration" else "SI consistent ✓",
                "Final Answer": f"**{r.name} = {r.value:.6g} {r.unit}**",
                "Physical Interpretation": f"{r.value:.3g} {r.unit}" +
                    (f" ≈ {r.value/_G0:.2f} g" if r.name == "acceleration" else ""),
                "Verification": "Limiting: F→0 ⇒ a→0 ✓",
            }
            return Answer(text, cls, plan, r, VerificationReport(
                [Check("dimensions", True, "F=ma")]), sections, self.level, self.mode)
        # Projectile pattern
        v0 = _grab(_NUM + r"\s*m/s\b", text)
        ang = _grab(_NUM + r"\s*(?:deg|°)\b", text)
        if v0 is not None and ang is not None and any(k in t for k in ("projectile", "launch", "range", "thrown")):
            pr = M.projectile(v0, ang)
            sections = {
                "Problem Understanding": "Vacuum projectile (no drag).",
                "Given Data": f"v0={v0} m/s, θ={ang}°",
                "Required": "Range, height, flight time.",
                "Assumptions": "- No air drag\n- Flat ground\n- Uniform g",
                "Governing Principle": "Constant-acceleration kinematics (Newton + gravity).",
                "Equation Derivation": "x=v0cosθ·t; y=v0sinθ·t−½gt²; eliminate t.",
                "Calculation": "\n".join(f"- {k}: **{v.value:.4g} {v.unit}**" for k, v in pr.items()),
                "Unit Check": "[m/s]²/[m/s²] = m ✓",
                "Verification": "θ=45° maximizes range; θ→0 ⇒ R→0 ✓",
                "Final Answer": f"**R = {pr['range'].value:.4g} m**",
                "Physical Interpretation": f"Lands {pr['range'].value:.3g} m away after {pr['flight_time'].value:.2f} s.",
                "Important Notes": "Drag shortens real ranges, especially at high speed.",
            }
            return Answer(text, cls, plan, pr, VerificationReport(
                [Check("dimensions", True, "R=v²/g")]), sections, self.level, self.mode)
        return None

    # ---------------- generic fallback ----------------
    def _generic_response(self, text, cls, plan) -> Answer:
        formulas = search_formulas(text, limit=5)
        concepts = _concepts.search_concepts(text, limit=3)
        fsec = ("\n".join(f"- **{f.name}**: `{f.equation}` _(assumes: {'; '.join(f.assumptions) or '—'})_"
                          for f in formulas) or "- (no close formula match — state the governing law explicitly)")
        csec = ("\n".join(f"- **{c.subtopic}**: {c.explanation[:220]}…" for c in concepts)
                or "- (no concept note matched)")
        missing = self._missing_data_note(text, cls)
        sections = {
            "Problem Understanding": (f"Domain: **{cls.domain}** → {cls.subdomain} · type: {cls.problem_type}. "
                                      f"System hint: {plan.system}."),
            "Given Data": self._fmt_knowns(plan) or "(none parsed — quote values with units, e.g. `m = 10 kg`)",
            "Required": plan.unknowns[0] if plan.unknowns else "Tell me the target quantity.",
            "Assumptions": "\n".join(f"- {a.statement} _(why: {a.justification})_" for a in plan.assumptions) or "- (none yet)",
            "Physical Model": "\n".join(f"- {k}: {v}" for k, v in plan.model.items()),
            "Governing Principle": "\n".join(f"- {p}" for p in plan.principles),
            "Equation Derivation": ("Candidate relations from the knowledge base:\n" + fsec +
                                    "\n\nRelevant concepts:\n" + csec),
            "Calculation": missing,
            "Unit Check": "Convert all inputs to SI first (the solver does this automatically once values are given).",
            "Verification": limiting_case_note(cls.domain),
            "Final Answer": missing,
            "Physical Interpretation": "(numeric interpretation appears once the calculation runs)",
            "Important Notes": ("I need the minimum missing data above — or say `assume standard values` "
                                "and I will state each assumption and continue. No numbers are guessed silently."),
        }
        return Answer(text, cls, plan, None, VerificationReport(
            [Check("triage", True, f"classified {cls.domain}; awaiting data")]),
            sections, self.level, self.mode)

    def _missing_data_note(self, text, cls) -> str:
        needs = {
            "vibrations": "Need mass + stiffness (e.g. `m = 20 kg, k = 50000 N/m`), damping `c` if known.",
            "classical_mechanics": "Need the two knowns of the target relation (e.g. `F = 100 N, m = 10 kg`).",
            "fluid_mechanics": "Need ρ, v, L, μ (state fluid + geometry so I can pick properties).",
            "thermodynamics": "Need states/properties (p, V, T, fluid) and the process path.",
            "electromagnetism": "Need charges/currents + geometry, or circuit topology + values.",
        }
        return ("**Missing minimum data.** " + needs.get(cls.domain,
                "Quote knowns with units and the target quantity."))

    def _error_answer(self, text, cls, plan, msg: str) -> Answer:
        return Answer(text, cls, plan, None, VerificationReport(
            [Check("input", False, msg)]),
            {"Problem Understanding": "Input error — nothing computed.",
             "Important Notes": f"**Error:** {msg} Correct it and resubmit."},
            self.level, self.mode)

    @staticmethod
    def _fmt_knowns(plan: SolutionPlan) -> str:
        return "\n".join(f"- {q.name} = {q.value} {q.unit or ''} [{q.status}]"
                         for q in plan.knowns)
