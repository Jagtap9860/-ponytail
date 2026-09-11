# Council Log — Chapter 1 trial notes

**Date:** 2026-09-11 · **Reader brief:** recent MechE grad, basic vibrations (SDOF) only.
**Source:** Ch.1 §§1.1–1.9 (plate story → FRF → hammer/shaker → windows →
curvefit → modal-vs-operating). Notes paraphrased, not quoted.

## Round 1 — DRAFT (lens owners)

- **Meera** (theory spine): modal-independence argument (characteristics vs
  loads vs spec), FRF matrix + reciprocity, node rule, ODS = linear combination
  of modes. Insisted the "dwell shape ≈ mode shape" approximation be labelled.
- **Viktor** (lab truth): drive-point checklist, roving-mass + stinger gotchas,
  tip/decay/coherence pre-flight, double-hit + saturation warnings, lab checklist.
- **Lena** (signal chain): analyzer chain table, leakage-first explanation,
  window selection table + costs, burst/chirp vs random verdict.
- **Arjun** (pedagogy): §0 SDOF→modes primer, kitchen/ruler/swing bridges,
  micro-examples (imag-peak reading, window drill), self-test + answers,
  revision sheet, glossary.
- **Sofia** (field): modal-vs-operating decision table, SDM/FEM payoff framing,
  cabin-drone mini-case, "pain vs cure" rule.

## Round 2 — CROSS-EXAMINATION (the fights)

| # | Challenger → Owner | Claim challenged | Verdict |
|---|---|---|---|
| 1 | Arjun → Meera | "Deformation at dwell = mode shape" stated flatly | **FIXED** — now labelled ≈ with neighbor-leakage note |
| 2 | Meera → Arjun | Swing analogy might imply modes are uncoupled pendulums | **FIXED** — tied-swings = coupled; kept with coupling line |
| 3 | Sofia → Viktor | "Impact dodges all shaker problems" over-claim | **FIXED** — impact has own enemies (tip, double hits); table rebalanced |
| 4 | Lena → Meera | Reciprocity stated without condition | **FIXED** — symmetric M/C/K condition added |
| 5 | Meera → Lena | "Windows = tax" hides that windows add damping bias | **FIXED** — amplitude + damping cost stated in §1.6 |
| 6 | Viktor → Sofia | Cabin case numbers could read as measured data | **FIXED** — labelled illustrative mini-case |
| 7 | Arjun → Lena | "Coherence = quality meter" too vague for a fresher | **FIXED** — defined as output-fraction-from-input, with ≪1 rule |

Refuted filings: 0. All 7 challenges confirmed and fixed in the notes.

## Round 3 — VERDICT

- **Ship gates:** completeness (1.1–1.9) ✔ · primer ✔ · examples ✔ ·
  visuals/tables ✔ · revision + glossary + self-test ✔ · honesty (no verbatim
  lifts, approximations labelled) ✔. `check_notes.py` passes.
- **Awards:** *Sharpest Blade* — Arjun (3 confirmed catches) · *Glass Jaw* —
  nobody (all drafts survived cross-exam) · *Student's Friend* — Arjun (§0 primer).
- **Carried to Ch.2:** keep §0-style primer per chapter; add one "link-back"
  line per section ("which Ch.1 picture does this formalize?").

*Signed: Meera ✔ · Viktor ✔ · Lena ✔ · Arjun ✔ · Sofia ✔*
