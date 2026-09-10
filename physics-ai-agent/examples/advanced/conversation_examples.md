# Example conversations

## 1. Direct solution (default)

> USER: A 10 kg mass is attached to a spring with k = 500 N/m. Find its natural frequency.

> AGENT: *(13-section report, shortened for low complexity)*
> **Final Answer: fn = 1.125 Hz (ωn = 7.071 rad/s), ζ = 0**
> …derivation ωn=√(k/m), unit check [N/m÷kg]^½=rad/s, limiting case ζ→0…

## 2. Engineering triage

> USER: I have a 20 kg machine mounted on a spring with stiffness 50,000 N/m and
> damping coefficient 100 Ns/m. What is its natural frequency and resonance behavior?

> AGENT: **fn = 7.958 Hz, ζ = 0.05**; Q≈10; avoid dwell near 8 Hz; r>√2 isolates;
> sensitivity table for k±10%; FRF plot on request.

## 3. Resonance discussion (not just "close = resonance")

> USER: My ANSYS modal analysis shows 217 Hz while excitation is 215 Hz. What does this mean?

> AGENT: 0.92% margin = HIGH concern, **but** proximity is necessary, not sufficient —
> checks: participation/direction, measured ζ, dwell time, linearity, fn scatter;
> actions: harmonic analysis with real damping, separation redesign, modal test.

## 4. Guided (Socratic)

> USER: *(mode=guided)* A 10 kg mass, k = 500 N/m. Find fn.

> AGENT: Classified as vibrations → SDOF free vibration. Given m, k.
> **Your turn:** What physical law gives M·x¨ + C·x˙ + K·x = F(t)?

## 5. Exam (no reveal)

> USER: *(mode=exam)* F = 100 N, m = 10 kg. Find a.

> AGENT: …**Hint:** Draw the free-body diagram first: what forces act, and along which axes?

## 6. Missing data (no silent guessing)

> USER: What is the vibration of my machine?

> AGENT: **Missing minimum data.** Need mass + stiffness (e.g. `m = 20 kg,
> k = 50000 N/m`), damping `c` if known — or say `assume standard values`.
