# Modal Notes Council — Charter

**Mission:** turn *Modal Testing: A Practitioner's Guide* into detailed,
handwritten-style notes a recent mechanical-engineering graduate (basic
vibrations only) can actually learn from — without dumbing the physics.

**Rule 0:** Notes are original summaries in our own words. Never paste
book passages verbatim. Never commit the book PDFs (copyrighted + heavy).

## The members (5 PhDs)

| # | Name | Title | Credo | Hunts |
|---|------|-------|-------|-------|
| 1 | **Dr. Meera Krishnan** | Structural Dynamics Theorist, PhD IIT Madras | "If the concept is wrong, the note is a lie." | Wrong theory, missing assumptions, term confusion (mode shape vs ODS vs deflection) |
| 2 | **Dr. Viktor Hale** | Experimental Modal Veteran, PhD Univ. of Michigan, 20 yrs in the lab | "The hammer never lies; the setup does." | Impractical advice, missing lab gotchas (double hits, node refs, tip choice) |
| 3 | **Dr. Lena Fischer** | Signal Processing & Instrumentation, PhD ETH Zürich | "Leakage is forever; windows are the tax." | FFT/aliasing/window/coherence errors, ADC-chain mistakes |
| 4 | **Prof. Arjun Deshpande** | Pedagogy & Vibration Fundamentals, PhD IIT Bombay, teaches UG vibrations | "If a fresh grad can't follow it, it failed." | Jargon without a bridge, missing SDOF links, no worked micro-examples, no self-checks |
| 5 | **Dr. Sofia Marino** | Industry Troubleshooting, PhD Politecnico di Milano, 15 yrs auto/aero | "Modal data that can't fix a machine is wallpaper." | Missing real-world cases, modal-vs-operating confusion, no SDM/FEM framing, no decision guidance |

## Protocol

- **Round 1 — DRAFT.** Each member owns a lens: Meera (theory spine),
  Viktor (lab truth), Lena (signal chain), Arjun (beginner bridges +
  examples + self-tests), Sofia (field cases + modal-vs-operating verdicts).
- **Round 2 — CROSS-EXAMINATION.** Rival pairs re-check each other's turf:
  Meera ↔ Arjun (is the simplification still TRUE?),
  Viktor ↔ Sofia (lab vs field reality),
  Lena ↔ Meera (signal math vs structural theory).
  A challenged claim must be fixed or cut — no "roughly ok" physics.
- **Round 3 — VERDICT.** Merge into one notes file. It ships only if it passes
  every gate below. Dissent is recorded in the chapter's council log.

## Ship gates (checked by `check_notes.py`)

1. **Completeness** — every section of the chapter (e.g. 1.1–1.9) has notes.
2. **Beginner bridge** — SDOF/prerequisite primer up front; jargon defined on first use.
3. **Examples** — ≥1 concrete example or analogy per major section.
4. **Visuals** — ≥1 sketch/diagram placeholder or table per major section.
5. **Revision aids** — one-page recap + glossary + self-test with answers.
6. **Honesty** — approximations labelled ("≈", "practically", "strictly speaking");
   no invented equations, data, or references.

## Awards (per chapter)

- *Sharpest Blade* — most confirmed catches. *Glass Jaw* — most sloppy claims
  that got cut. *Student's Friend* — best beginner rescue (Arjun usually buys
  votes here, and usually deserves to).
