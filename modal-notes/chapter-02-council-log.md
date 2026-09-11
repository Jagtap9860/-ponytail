# Council Log — Chapter 2 notes

**Date:** 2026-09-11 · **Reader brief:** recent MechE grad, basic vibrations (SDOF) only.
**Source:** Ch.2 §§2.1–2.4 (FEM-vs-EMA → SDOF theory → MDOF theory → full-loop
summary). Notes paraphrased; all figures redrawn as original sketches.

## Round 1 — DRAFT (lens owners)

- **Meera** (theory spine): pole anatomy, S-plane migration, force-balance
  regimes, Laplace 3-forms equivalence, residue-as-DNA, orthogonality,
  modal transformation, global poles, FRF summation (residue + shape faces).
- **Viktor** (lab truth): half-power/log-dec "museum methods" framing,
  drive-point tour (h33/h32/h31), row-vs-column derivation, theory-to-lab
  checklist, EX6 hand-estimation.
- **Lena** (signal chain): Bode/co-quad/Nyquist portraits, Nyquist-circle
  quality rule, D/V/A slope detective kit, 90° resonance signature.
- **Arjun** (pedagogy): §0 Ch.1→Ch.2 bridge table, S-plane-without-Laplace
  map analogy, EX1–EX7 worked numbers, self-test + answers, glossary.
- **Sofia** (field): FEM-vs-EMA loop economics, turbine-blade superposition
  story, truncation/residuals payoff, 88-vs-82-Hz mismatch drill.

## Round 2 — CROSS-EXAMINATION (the fights)

| # | Challenger → Owner | Claim challenged | Verdict |
|---|---|---|---|
| 1 | Meera → Arjun | Shape-form FRF shown without conditions | **FIXED** — proportional-damping + modal-mass scaling noted (eigensolution section) |
| 2 | Arjun → Meera | "Cities on a map" hides that poles move with design changes | **FIXED** — stiffness-pushes-north / damping-pushes-west lines added |
| 3 | Viktor → Lena | Half-power presented as a working method | **FIXED** — reframed as sanity-check/interview tool; estimators crowned |
| 4 | Lena → Viktor | "Nyquist potato" rule too folksy to trust | **CONFIRMED AS-IS** — kept, with 3-suspect list (overlap/noise/nonlinearity) in self-test |
| 5 | Sofia → Meera | Eigensolver name-dropping without guidance | **FIXED** — small-direct vs large-iterative split added |
| 6 | Meera → Sofia | Turbine numbers could read as measured data | **FIXED** — labelled illustrative book-style walk-through |
| 7 | Arjun → Lena | A/F=−ω²D/F sign confusing for freshers | **FIXED** — "180° apart, scaled by ω²" phrasing + EX4 drill |
| 8 | Viktor → Meera | Node-rule "birth certificate" claim too strong for non-proportional damping | **FIXED** — claim scoped to the book's proportional-damping theory |

Refuted filings: 0. All 8 challenges resolved in the notes.

## Round 3 — VERDICT

- **Ship gates:** completeness (2.1–2.4) ✔ · primer ✔ · examples (7 worked
  EX + drills) ✔ · visuals (11 original sketches + 9 tables) ✔ · revision +
  glossary + self-test ✔ · honesty (linearity clause, illustrative-numbers
  labels) ✔. `check_notes.py` passes Ch.1 + Ch.2.
- **Awards:** *Sharpest Blade* — Meera (3 confirmed catches) · *Glass Jaw* —
  nobody · *Student's Friend* — Arjun (EX1–EX7 ladder).
- **Carried to Ch.3:** keep the worked-number ladder; add one "plot detective"
  drill per chapter (slopes trick was the review favorite).

## Round 4 — EXTENDED EDITION (user: "too short, do better, no padding")

- **Charge:** 12 pages → 40+ pages of GENUINE content. No filler allowed.
- **Delivered:** 41-page PDF (`make_ch2_full.py`): 9 Deep-cut chapters (proofs,
  damping lab, zeros/synthesis, Bode/transients, quotient/absorber/stability,
  capstone), 34 worked examples EX-A…EX-AI (all numbers hand-verified:
  2DOF masterclass, anti-resonance wz=10.0, phase-flip synthesis, Rayleigh fit,
  isolation 88%, quotient bound 38.46), 23 original sketches, 3 MD banks.
- **Fights:** Meera caught P15's ζ (6.4% → 9.1% recompute) · Viktor demanded the
  5-route static cross-check before sign-off · Lena insisted on the
  resolution→Ch.3 bridge table · Arjun cut 2 planned pages as "padding-adjacent".
- **Verdict:** every page earned. Ship gates re-passed (`check_notes.py` Ch.1+Ch.2 ✔).

*Signed: Meera ✔ · Viktor ✔ · Lena ✔ · Arjun ✔ · Sofia ✔*
*Signed: Meera ✔ · Viktor ✔ · Lena ✔ · Arjun ✔ · Sofia ✔ (R3 above; R4 countersigned)*
