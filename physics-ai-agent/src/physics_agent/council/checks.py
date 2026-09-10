"""Deterministic check batteries — one per Council member.

Every check returns Findings with reproducible evidence and a recheck closure
so Round 2 rivals can independently verify. No finding without reproduction.
"""
from __future__ import annotations

import ast
import json
import math
import subprocess
import sys
from pathlib import Path

from physics_agent.council.findings import Finding

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC = PROJECT_ROOT / "src" / "physics_agent"
DATA = PROJECT_ROOT / "data"
CLI = [sys.executable, "-m", "physics_agent.cli"]

_fid = 0


def _new(persona: str, severity: str, title: str, location: str,
         evidence: str, recheck, user_facing: bool = False) -> Finding:
    global _fid
    _fid += 1
    return Finding(f"{persona.upper()}-{_fid:02d}", persona, severity, title,
                   location, evidence, recheck, user_facing)


def run_cli(*args: str, timeout: int = 180) -> subprocess.CompletedProcess:
    """Council check: Run cli."""
    return subprocess.run([*CLI, *args], capture_output=True, text=True,
                          cwd=PROJECT_ROOT, timeout=timeout)


def _src_files() -> list[Path]:
    return sorted(p for p in SRC.rglob("*.py") if "__pycache__" not in p.parts)


# =====================================================================
# Dr. Vex — physics correctness
# =====================================================================

def vex_formula_schema() -> list[Finding]:
    """Council check: Vex formula schema."""
    out: list[Finding] = []
    for f in sorted((DATA / "formulas").glob("*.json")):
        try:
            rows = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            out.append(_new("vex", "critical", "Formula file is not valid JSON",
                            str(f.relative_to(PROJECT_ROOT)), repr(e),
                            lambda f=f: _json_broken(f), True))
            continue
        bad = [str(r.get("name", r)) for r in rows
               if not all(k in r for k in ("name", "equation", "domain", "variables"))
               or not r.get("variables")]
        if bad:
            out.append(_new("vex", "high", "Formula entries missing required schema fields",
                            str(f.relative_to(PROJECT_ROOT)),
                            f"{len(bad)} bad entries: {bad[:3]}",
                            lambda f=f: _schema_broken(f), True))
    return out


def _json_broken(f: Path) -> bool:
    try:
        json.loads(f.read_text(encoding="utf-8"))
        return False
    except Exception:
        return True


def _schema_broken(f: Path) -> bool:
    try:
        rows = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return True
    return any(not all(k in r for k in ("name", "equation", "domain", "variables"))
               or not r.get("variables") for r in rows)


def vex_constants() -> list[Finding]:
    """Council check: Vex constants."""
    from physics_agent.knowledge.constants import get_constant
    spot = {"c": 299792458.0, "g0": 9.80665, "h": 6.62607015e-34,
            "kB": 1.380649e-23, "e": 1.602176634e-19, "NA": 6.02214076e23,
            "R": 8.31446261815324, "sigma": 5.670374419e-8}
    out: list[Finding] = []
    for sym, want in spot.items():
        try:
            got = get_constant(sym).value
            ok = math.isclose(got, want, rel_tol=1e-9)
        except KeyError:
            got, ok = None, False
        if not ok:
            out.append(_new("vex", "critical", f"Constant '{sym}' wrong or missing",
                            "data/constants/codata2022.json",
                            f"got {got}, want {want}",
                            lambda s=sym, w=want: not _const_ok(s, w), True))
    return out


def _const_ok(sym: str, want: float) -> bool:
    from physics_agent.knowledge.constants import get_constant
    try:
        return math.isclose(get_constant(sym).value, want, rel_tol=1e-9)
    except KeyError:
        return False


def vex_solver_spots() -> list[Finding]:
    """Council check: Vex solver spots."""
    from physics_agent.physics import electromagnetism as EM
    from physics_agent.physics import mechanics as ME
    from physics_agent.physics import quantum as QM
    from physics_agent.physics import thermo as TH
    from physics_agent.physics import vibrations as VI
    spots = [
        ("SDOF fn", lambda: VI.sdof_free(10.0, 500.0)["fn"].value, 1.1253954, 1e-6,
         "physics/vibrations.py::sdof_free"),
        ("machine zeta", lambda: VI.sdof_free(20.0, 50000.0, 100.0)["zeta"].value, 0.05, 1e-12,
         "physics/vibrations.py::sdof_free"),
        ("projectile 45°", lambda: ME.projectile(20, 45)["range"].value, 20**2 / 9.80665, 1e-9,
         "physics/mechanics.py::projectile"),
        ("coulomb sign", lambda: EM.coulomb(1e-6, -1e-6, 1.0).value, -0.0089875517923, 1e-6,
         "physics/electromagnetism.py::coulomb"),
        ("green photon", lambda: QM.photon_energy(lam=532e-9)["energy_eV"].value, 2.3305, 1e-3,
         "physics/quantum.py::photon_energy"),
        ("carnot", lambda: TH.carnot_efficiency(600, 300).value, 0.5, 1e-12,
         "physics/thermo.py::carnot_efficiency"),
    ]
    out: list[Finding] = []
    for name, fn, want, tol, loc in spots:
        try:
            got, ok = fn(), None
            ok = math.isclose(got, want, rel_tol=tol)
        except Exception as e:  # noqa: BLE001
            got, ok = f"RAISED {e!r}", False
        if not ok:
            out.append(_new("vex", "critical", f"Solver physics wrong: {name}", loc,
                            f"got {got}, want {want}",
                            lambda f=fn, w=want, t=tol: not _spot_ok(f, w, t), True))
    return out


def _spot_ok(fn, want: float, tol: float) -> bool:
    try:
        return math.isclose(fn(), want, rel_tol=tol)
    except Exception:
        return False


# Physical-constant literals that must come from knowledge.constants, never code.
_BANNED_LITERALS = (9.80665, 299792458, 6.62607015e-34, 1.054571817e-34,
                    1.380649e-23, 1.602176634e-19, 8.8541878128e-12,
                    1.25663706212e-6, 6.6743e-11, 5.670374419e-8,
                    6.02214076e23, 8.31446261815324, 8987551792.3)


def _literal_hits(path: Path) -> list[tuple[int, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
                and not isinstance(node.value, bool):
            for banned in _BANNED_LITERALS:
                if node.value == banned or (
                        isinstance(node.value, float)
                        and math.isclose(node.value, banned, rel_tol=1e-12)):
                    hits.append((node.lineno, repr(node.value)))
    return hits


def vex_hardcoded_constants() -> list[Finding]:
    """Council check: Vex hardcoded constants."""
    out: list[Finding] = []
    for p in _src_files():
        if p.parent.name == "knowledge" or p.parent.name == "council":
            continue  # the database itself + this very check may name them
        hits = _literal_hits(p)
        if hits:
            out.append(_new("vex", "medium", "Hard-coded physical constant (use knowledge.constants)",
                            f"{p.relative_to(PROJECT_ROOT)}:{hits[0][0]}",
                            f"{len(hits)} literal(s): {hits[:3]}",
                            lambda p=p: bool(_literal_hits(p))))
    return out


# =====================================================================
# Prof. Null — numerical integrity
# =====================================================================

def null_fft() -> list[Finding]:
    """Council check: Null fft."""
    import numpy as np
    from physics_agent.solvers.spectral import fft_spectrum
    t = np.arange(0, 1, 0.001)
    s = fft_spectrum(np.sin(2 * math.pi * 50 * t), 0.001)
    ok = math.isclose(s.peak_freq, 50.0, rel_tol=1e-9) and math.isclose(s.peak_amplitude, 1.0, rel_tol=0.05)
    if ok:
        return []
    return [_new("null", "high", "FFT peak wrong", "solvers/spectral.py::fft_spectrum",
                 f"peak {s.peak_freq} Hz / {s.peak_amplitude}",
                 lambda: not _fft_ok(), True)]


def _fft_ok() -> bool:
    import numpy as np
    from physics_agent.solvers.spectral import fft_spectrum
    t = np.arange(0, 1, 0.001)
    s = fft_spectrum(np.sin(2 * math.pi * 50 * t), 0.001)
    return math.isclose(s.peak_freq, 50.0, rel_tol=1e-9)


def null_ode() -> list[Finding]:
    """Council check: Null ode."""
    from physics_agent.solvers.ode import solve_sdof
    r = solve_sdof(1.0, 0.0, 4.0, t_end=math.pi, n=2000, x0=1.0)
    ok = r.success and math.isclose(r.y[0, -1], math.cos(2 * math.pi), abs_tol=1e-3)
    if ok:
        return []
    return [_new("null", "high", "ODE solver disagrees with analytic solution",
                 "solvers/ode.py::solve_sdof", f"x(pi)={r.y[0, -1]}",
                 lambda: not _ode_ok(), True)]


def _ode_ok() -> bool:
    from physics_agent.solvers.ode import solve_sdof
    r = solve_sdof(1.0, 0.0, 4.0, t_end=math.pi, n=2000, x0=1.0)
    return r.success and math.isclose(r.y[0, -1], math.cos(2 * math.pi), abs_tol=1e-3)


def null_guards() -> list[Finding]:
    """Council check: Null guards."""
    from physics_agent.mathematics.differential_equations import (
        heat_equation_explicit,
        wave_equation_leapfrog,
    )
    from physics_agent.physics import mechanics as ME
    from physics_agent.physics import optics_waves as OW
    from physics_agent.physics import relativity as RE
    cases = [
        ("heat stability guard", lambda: heat_equation_explicit(T=1.0, nx=11, nt=10, alpha=1.0)),
        ("wave CFL guard", lambda: wave_equation_leapfrog(L=1.0, T=1.0, nx=11, nt=10, c=100.0)),
        ("v >= c rejected", lambda: RE.lorentz_factor(299792458.0)),
        ("negative stiffness rejected", lambda: ME.cantilever_tip(1, 1, -1, 1)),
        ("TIR raises (no silent NaN)", lambda: OW.snell(1.5, 60.0, 1.0)),
    ]
    out: list[Finding] = []
    for name, fn in cases:
        try:
            fn()
            raised = False
        except (ValueError, ZeroDivisionError):
            raised = True
        except Exception:  # noqa: BLE001 - wrong exception type is also a finding
            raised = False
        if not raised:
            out.append(_new("null", "high", f"Missing guard: {name}",
                            "solvers|physics (input validation)", "no ValueError raised",
                            lambda f=fn: not _raises_value(f)))
    return out


def _raises_value(fn) -> bool:
    try:
        fn()
        return False
    except ValueError:
        return True
    except Exception:
        return False


# =====================================================================
# Major Merge — software product bar
# =====================================================================

def merge_entrypoint() -> list[Finding]:
    """Council check: Merge entrypoint."""
    from importlib import metadata
    try:
        eps = metadata.entry_points(group="console_scripts")
        hit = [e for e in eps if e.name == "physics-agent"]
    except Exception:  # noqa: BLE001
        hit = []
    if hit:
        return []
    # Static fallback: declared in pyproject AND attribute exists?
    declared = "physics-agent" in (PROJECT_ROOT / "pyproject.toml").read_text()
    from physics_agent import cli as _cli
    exists = callable(getattr(_cli, "main", None))
    if declared and exists:
        return [_new("merge", "medium", "physics-agent entry point not installed in this env",
                     "pyproject.toml [project.scripts]",
                     "declared + callable, but no console_script metadata — reinstall",
                     lambda: not _ep_ok(), True)]
    return [_new("merge", "critical", "physics-agent CLI entry point broken",
                 "pyproject.toml [project.scripts]",
                 f"declared={declared} callable={exists}",
                 lambda: not _ep_ok(), True)]


def _ep_ok() -> bool:
    from importlib import metadata
    try:
        return any(e.name == "physics-agent" for e in metadata.entry_points(group="console_scripts"))
    except Exception:
        return False


def _annotation_coverage() -> tuple[float, list[str]]:
    total, ok, offenders = 0, 0, []
    for p in _src_files():
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("_") and node.name != "__init__":
                continue
            total += 1
            args = [a for a in node.args.args if a.arg not in ("self", "cls")]
            args += list(node.args.kwonlyargs)
            typed = all(a.annotation is not None for a in args) and (
                node.returns is not None or node.name == "__init__")
            if typed:
                ok += 1
            else:
                offenders.append(f"{p.name}:{node.name}")
    return (ok / total if total else 1.0), offenders


def merge_typing() -> list[Finding]:
    """Council check: Merge typing."""
    cov, offenders = _annotation_coverage()
    if cov >= 0.90:
        return []
    return [_new("merge", "medium", f"Type-hint coverage {cov:.0%} < 90%",
                 "src/physics_agent/**",
                 f"untyped: {offenders[:5]}",
                 lambda: _annotation_coverage()[0] < 0.90)]


def _docstring_coverage() -> tuple[float, list[str]]:
    total, ok, offenders = 0, 0, []
    for p in _src_files():
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for node in [tree, *[n for n in ast.walk(tree)
                           if isinstance(n, (ast.FunctionDef, ast.ClassDef))]]:
            name = getattr(node, "name", "<module>")
            if isinstance(node, ast.FunctionDef) and name.startswith("_") and name != "__init__":
                continue
            total += 1
            if ast.get_docstring(node):
                ok += 1
            else:
                offenders.append(f"{p.name}:{name}")
    return (ok / total if total else 1.0), offenders


def merge_docstrings() -> list[Finding]:
    """Council check: Merge docstrings."""
    cov, offenders = _docstring_coverage()
    if cov >= 0.90:
        return []
    return [_new("merge", "low", f"Docstring coverage {cov:.0%} < 90%",
                 "src/physics_agent/**", f"missing: {offenders[:5]}",
                 lambda: _docstring_coverage()[0] < 0.90)]


def merge_license() -> list[Finding]:
    """Council check: Merge license."""
    lic = PROJECT_ROOT / "LICENSE"
    if lic.exists() and "MIT" in lic.read_text(encoding="utf-8"):
        return []
    return [_new("merge", "critical", "LICENSE file missing (pyproject claims MIT)",
                 "LICENSE", "file absent or not MIT",
                 lambda: not ((PROJECT_ROOT / "LICENSE").exists()), True)]


def merge_gitignore() -> list[Finding]:
    """Council check: Merge gitignore."""
    required = [".venv/", "build/", "dist/", ".pytest_cache/", ".ruff_cache/",
                "__pycache__/", ".env"]
    gi = PROJECT_ROOT / ".gitignore"
    have = gi.read_text(encoding="utf-8") if gi.exists() else ""
    missing = [r for r in required if r not in have]
    if not missing:
        return []
    return [_new("merge", "high", ".gitignore missing entries",
                 ".gitignore", f"missing: {missing}",
                 lambda: _gi_missing(), True)]


def _gi_missing() -> bool:
    required = [".venv/", "build/", "dist/", ".pytest_cache/", ".ruff_cache/",
                "__pycache__/", ".env"]
    gi = PROJECT_ROOT / ".gitignore"
    have = gi.read_text(encoding="utf-8") if gi.exists() else ""
    return any(r not in have for r in required)


def merge_prints() -> list[Finding]:
    """Council check: Merge prints."""
    out: list[Finding] = []
    for p in _src_files():
        if p.name == "cli.py":
            continue  # CLI is allowed to talk
        tree = ast.parse(p.read_text(encoding="utf-8"))
        n = sum(1 for node in ast.walk(tree)
                if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "print")
        if n:
            out.append(_new("merge", "low", f"print() in library code ({n}x)",
                            str(p.relative_to(PROJECT_ROOT)),
                            "library must return, not print",
                            lambda p=p: _has_print(p)))
    return out


def _has_print(p: Path) -> bool:
    tree = ast.parse(p.read_text(encoding="utf-8"))
    return any(isinstance(n, ast.Call) and getattr(n.func, "id", "") == "print"
               for n in ast.walk(tree))


def merge_tools() -> list[Finding]:
    """Council check: Merge tools."""
    from physics_agent.tools import TOOLS
    broken = [n for n, t in TOOLS.items()
              if not (t.description and t.parameters and callable(t.function))]
    if not broken and len(TOOLS) >= 10:
        return []
    return [_new("merge", "high", "Tool registry entries malformed",
                 "tools/registry.py", f"broken={broken} count={len(TOOLS)}",
                 lambda: _tools_broken(), True)]


def _tools_broken() -> bool:
    from physics_agent.tools import TOOLS
    return any(not (t.description and t.parameters and callable(t.function))
               for t in TOOLS.values()) or len(TOOLS) < 10


# =====================================================================
# Agent Chaos — adversarial inputs
# =====================================================================

def chaos_api_abuse() -> list[Finding]:
    """Council check: Chaos api abuse."""
    from physics_agent.agent.orchestrator import Orchestrator
    from physics_agent.tools import call_tool
    from physics_agent.units.converter import convert
    cases = [
        ("unknown unit raises ValueError", lambda: convert(1, "furlongs", "m"), ValueError),
        ("empty problem raises ValueError", lambda: Orchestrator().solve(""), ValueError),
        ("empty problem (spaces)", lambda: Orchestrator().solve("   "), ValueError),
        ("unknown tool raises KeyError", lambda: call_tool("teleport"), KeyError),
    ]
    out: list[Finding] = []
    for name, fn, exc in cases:
        try:
            fn()
            got = "no exception"
        except exc:
            continue
        except Exception as e:  # noqa: BLE001
            got = f"wrong exception: {type(e).__name__}"
        out.append(_new("chaos", "high", f"API abuse not handled: {name}",
                        "units|agent|tools", got,
                        lambda f=fn, e=exc: not _raises(f, e), True))
    # nonsense must NOT raise — graceful triage
    try:
        ans = Orchestrator().solve("asdf qwer zxcv blah")
        graceful = ans is not None and "Missing minimum data" in ans.report()
    except Exception as e:  # noqa: BLE001
        graceful = False
    if not graceful:
        out.append(_new("chaos", "high", "Nonsense input crashes or mistrips triage",
                        "agent/orchestrator.py::solve", "expected graceful generic answer",
                        lambda: not _nonsense_ok(), True))
    return out


def _raises(fn, exc) -> bool:
    try:
        fn()
        return False
    except exc:
        return True
    except Exception:
        return False


def _nonsense_ok() -> bool:
    from physics_agent.agent.orchestrator import Orchestrator
    try:
        return "Missing minimum data" in Orchestrator().solve("asdf qwer zxcv blah").report()
    except Exception:
        return False


def chaos_cli_abuse() -> list[Finding]:
    """Council check: Chaos cli abuse."""
    out: list[Finding] = []
    r = run_cli("solve", "%%% ??? !!!")
    if r.returncode != 0 or "Traceback" in (r.stdout + r.stderr):
        out.append(_new("chaos", "high", "CLI crashes on garbage input",
                        "cli.py::solve", f"rc={r.returncode} {r.stderr[:200]}",
                        lambda: _cli_garbage_broken(), True))
    r = run_cli("solve", "")
    if r.returncode == 0 or "Traceback" in (r.stdout + r.stderr) or "error" not in (r.stdout + r.stderr).lower():
        out.append(_new("chaos", "high", "CLI empty-input path leaks or misbehaves",
                        "cli.py::solve", f"rc={r.returncode} {r.stderr[:200]}",
                        lambda: _cli_empty_broken(), True))
    return out


def _cli_garbage_broken() -> bool:
    r = run_cli("solve", "%%% ??? !!!")
    return r.returncode != 0 or "Traceback" in (r.stdout + r.stderr)


def _cli_empty_broken() -> bool:
    r = run_cli("solve", "")
    return r.returncode == 0 or "Traceback" in (r.stdout + r.stderr)


def chaos_physics_abuse() -> list[Finding]:
    """Council check: Chaos physics abuse."""
    from physics_agent.physics import mechanics as ME
    from physics_agent.physics import thermo as TH
    cases = [
        ("negative E", lambda: ME.cantilever_tip(1, 1, -3, 1)),
        ("negative mu", lambda: ME.incline_slide(1, 30, -0.5)),
        ("emissivity > 1", lambda: TH.radiation(2.0, 1, 300, 290)),
    ]
    out: list[Finding] = []
    for name, fn in cases:
        try:
            fn()
            raised = False
        except ValueError:
            raised = True
        except Exception:  # noqa: BLE001
            raised = False
        if not raised:
            out.append(_new("chaos", "medium", f"Unphysical input accepted: {name}",
                            "physics/*", "no ValueError",
                            lambda f=fn: not _raises_value(f), True))
    return out


def _raises_value(fn) -> bool:
    try:
        fn()
        return False
    except ValueError:
        return True
    except Exception:
        return False


# =====================================================================
# Scribe Nia — README honesty (regression net for review bugs #1–#4)
# =====================================================================

README_COMMANDS: list[tuple[tuple[str, ...], str]] = [
    (("solve", "A 10 kg mass is attached to a spring with k = 500 N/m. Find its natural frequency."),
     "Final Answer"),
    (("convert", "3000 rpm", "rad/s"), "314.159"),
    (("convert", "10 psi", "Pa"), "68947"),
    (("constants", "--search", "planck"), "Planck"),
    (("formulas", "--search", "natural frequency"), "natural frequency"),
    (("tools",), "convert_units"),
    (("demo", "machine-vibration"), "7.958 Hz"),
    (("demo", "resonance"), "0.92%"),
]


def nia_readme() -> list[Finding]:
    """Council check: Nia readme."""
    out: list[Finding] = []
    for args, want in README_COMMANDS:
        r = run_cli(*args)
        ok = r.returncode == 0 and want.lower() in (r.stdout + r.stderr).lower()
        if not ok:
            out.append(_new("nia", "critical",
                            f"README quick-start broken: physics-agent {' '.join(args)[:60]}",
                            "README.md", f"rc={r.returncode} want~{want!r} out={r.stdout[:150]!r}{r.stderr[:150]!r}",
                            lambda a=args, w=want: not _readme_ok(a, w), True))
    return out


def _readme_ok(args: tuple[str, ...], want: str) -> bool:
    r = run_cli(*args)
    return r.returncode == 0 and want.lower() in (r.stdout + r.stderr).lower()


def nia_help() -> list[Finding]:
    """Council check: Nia help."""
    r = run_cli("--help")
    missing = [c for c in ("solve", "chat", "convert", "constants", "formulas",
                           "tools", "demo", "council") if c not in r.stdout]
    if not missing and r.returncode == 0:
        return []
    return [_new("nia", "high", "CLI subcommands missing from --help",
                 "cli.py", f"missing={missing} rc={r.returncode}",
                 lambda: _help_broken(), True)]


def _help_broken() -> bool:
    r = run_cli("--help")
    subs = ("solve", "chat", "convert", "constants", "formulas", "tools", "demo", "council")
    return r.returncode != 0 or any(c not in r.stdout for c in subs)


def nia_docs() -> list[Finding]:
    """Council check: Nia docs."""
    missing = [d for d in ("architecture.md", "physics-methodology.md",
                           "contribution-guide.md", "council.md")
               if not (PROJECT_ROOT / "docs" / d).exists()]
    if not missing:
        return []
    return [_new("nia", "high", "Docs missing", "docs/",
                 f"missing={missing}",
                 lambda: _docs_missing(), True)]


def _docs_missing() -> bool:
    return any(not (PROJECT_ROOT / "docs" / d).exists()
               for d in ("architecture.md", "physics-methodology.md",
                         "contribution-guide.md", "council.md"))


def nia_examples() -> list[Finding]:
    """Council check: Nia examples."""
    import py_compile
    out: list[Finding] = []
    for p in sorted((PROJECT_ROOT / "examples").rglob("*.py")):
        try:
            py_compile.compile(str(p), doraise=True)
            ok = True
        except Exception as e:  # noqa: BLE001
            ok = f"{e}"
        if ok is not True:
            out.append(_new("nia", "high", "Example script does not compile",
                            str(p.relative_to(PROJECT_ROOT)), str(ok),
                            lambda p=p: _compile_broken(p), True))
    return out


def _compile_broken(p: Path) -> bool:
    import py_compile
    try:
        py_compile.compile(str(p), doraise=True)
        return False
    except Exception:
        return True


# Registry: persona -> checks (Round 1 hunt order).
CHECKS: list[tuple[str, object]] = [
    ("vex", vex_formula_schema), ("vex", vex_constants), ("vex", vex_solver_spots),
    ("vex", vex_hardcoded_constants),
    ("null", null_fft), ("null", null_ode), ("null", null_guards),
    ("merge", merge_entrypoint), ("merge", merge_typing), ("merge", merge_docstrings),
    ("merge", merge_license), ("merge", merge_gitignore), ("merge", merge_prints),
    ("merge", merge_tools),
    ("chaos", chaos_api_abuse), ("chaos", chaos_cli_abuse), ("chaos", chaos_physics_abuse),
    ("nia", nia_readme), ("nia", nia_help), ("nia", nia_docs), ("nia", nia_examples),
]
