# The Council — Adversarial Review Charter

Five reviewers. Zero mercy. Every line of code is guilty until proven innocent,
and every *finding* is challenged by a rival before it counts.

## The members

| # | Name | Title | Ego (credo) | Hunts |
|---|------|-------|-------------|-------|
| 1 | **Dr. Vex** | Theoretical Physicist | "If the physics is wrong, nothing else matters." | Wrong equations, bad constants, missing assumptions, dimensional lies |
| 2 | **Prof. Null** | Numerical Analyst | "It converges? Prove it. On *my* grid." | Instability, tolerance fraud, FFT sins, untested limits |
| 3 | **Major Merge** | Software Engineer | "Untyped, undocumented, unpackaged = a toy, not a product." | Packaging, typing, docs, packaging (yes, twice — it broke once) |
| 4 | **Agent Chaos** | Adversarial Tester | "I break things for breakfast." | Crashes, garbage input, silent wrong answers, traceback leaks |
| 5 | **Scribe Nia** | Docs & Honesty Auditor | "Docs lie. I catch them, with receipts." | README commands that don't run, phantom features, missing LICENSE |

## Protocol (enforced by `physics_agent.council`)

- **Round 1 — The Hunt.** Each member runs their deterministic check battery and
  files findings with severity, location, and reproducible evidence.
- **Round 2 — Cross-examination.** Every finding is assigned a *rival* who must
  (a) independently re-run the reproduction, and (b) vote on severity.
  A finding that doesn't reproduce is **REFUTED** (public humiliation for the
  author). Final severity = median of {author, rival₁, rival₂}, dissent recorded.
- **Round 3 — Verdict.** Scoreboard, required actions, and the round's awards:
  *Sharpest Blade* (most confirmed criticals), *Glass Jaw* (most refuted —
  named and shamed), *Overconfident* (failed refutations).

## Ego scoring

| Event | Points |
|---|---|
| Confirmed finding (critical/high/medium/low) | +4 / +3 / +2 / +1 to author |
| Successful refutation | +3 to rival |
| Failed refutation (finding reproduces anyway) | −1 to rival (overconfidence tax) |
| Refuted finding | −2 to author (filed a ghost) |

## Rules of engagement

1. No finding without reproduction. No reproduction, no points.
2. Severity is argued, never assumed — the median rules.
3. Fixing is separate from finding: the Council judges; the verdict lists
   required actions; a re-run must show zero open criticals/highs.
4. CI runs `physics-agent council review --fail-on critical` on every push.

Run it: `physics-agent council review` (add `--write council-report.md`).
