# Physics Methodology

How the agent solves every problem. Implemented by `agent/orchestrator.py`
with `reasoning.py`, `verification.py`, and `explanation.py`.

## The 10-step workflow

1. **Understand** — knowns, unknowns, system, units, implicit assumptions,
   domain. Ask for the minimum missing data; if a standard assumption
   unblocks the problem, state it and continue.
2. **Classify** — domain → sub-domain → problem type; mathematical and
   computational complexity; required equations/methods; symbolic vs
   numeric vs visual.
3. **Physical model** — geometry, coordinates, forces/moments, energy,
   BCs/ICs, materials, environment, constraints, applicable laws.
4. **Governing principles** — name the law(s) and justify *why* each applies.
   Never pattern-match formulas blindly.
5. **Derive** — force/energy/variational/matrix/tensor formulation as fits;
   math formulation precedes numerics on advanced problems.
6. **Dimensions & units** — SI consistency gate before any number is trusted.
7. **Symbolics first** — rearrange → substitute → evaluate, in that order.
8. **Numerics via tools** — roots, quadrature, ODEs, eigenproblems,
   optimization, fits, FFT, interpolation, Monte Carlo — all deterministic.
9. **Verify** — dimensional, limiting-case, order-of-magnitude, conservation,
   cross-derivation, analytic-vs-numeric, plausibility (see below).
10. **Interpret** — what the number *means* physically (comparisons, regimes).

## Verification battery (`agent/verification.py`)

- Dimensional check (dimension-vector equality).
- Limiting cases (e.g. c→0 recovers undamped; v≪c recovers Newtonian).
- Order-of-magnitude / plausibility bands per domain.
- Conservation-law residuals where applicable.
- Independent derivation (energy vs force route).
- Analytic-vs-numeric agreement (closed form vs `solve_ivp`/quadrature).
- Input-error scan: missing data, unit slips, sign conventions, impossible
  values (negative mass, |v|>c, η<0), unstable numerics, bad BCs,
  double-counted forces, non-inertial frames used as inertial.

## Provenance & integrity

Every statement is tagged: KNOWN physics / ASSUMPTION / APPROXIMATION /
CALCULATED / NEEDS EXPERIMENTAL VALIDATION. The agent never fabricates
equations, data, properties, references, or results; uncertainty is stated.
Safety-critical conclusions carry an explicit validation disclaimer.

## Response format (normal problems)

1. Problem Understanding 2. Given Data 3. Required 4. Assumptions
5. Physical Model 6. Governing Principle 7. Equation Derivation 8. Calculation
9. Unit Check 10. Verification 11. Final Answer 12. Physical Interpretation
13. Important Notes

Simple questions shorten automatically; research questions expand §7.

## Explanation levels & modes

Levels: 1 beginner · 2 engineering undergraduate · 3 advanced · 4 research.
Modes: `direct` (default), `guided` (Socratic), `teaching`, `exam`
(no solution reveal — hints only), `research`, `engineering` (design margins,
standards language, validation reminders). See `agent/modes.py`.

## Self-check before answering (advanced)

Problem understood · correct domain/law/equation · assumptions explicit ·
units consistent · numerics verified · result plausible · BCs considered ·
limits checked · no unsupported claims · explanation matches calculation.
