# 📓 Chapter 2 — General Theory of Experimental Modal Analysis
### *From Ch.1 pictures to the equations that run the lab* (detailed notes + extras)

> **Book:** *Modal Testing: A Practitioner's Guide* · **Chapter 2 ( §§2.1–2.4 )**
> **Reader:** recent MechE grad, basic vibrations (SDOF) · **Style:** handwritten-like.
> **Council verdict:** ✅ shipped (log: `chapter-02-council-log.md`)

**Legend:** 📌 key idea · 🧪 lab tip · ⚠️ trap · 🔗 bridge · ✍️ try it ·
📐 worked Example (EX1–EX7) · 🗣️ council voice · 🖼️ figure in the PDF twin

---

## §0 Primer — Ch.1 pictures → Ch.2 equations 🔗

| Ch.1 gave you the picture | Ch.2 gives you the machine |
|---|---|
| FRF peaks sit at natural frequencies | Poles `s = −ζωₙ ± jωd` — real part = damping, imag part = frequency |
| Imag-peak heights trace the shape | Residues `Aᵢⱼᵣ ∝ uᵢᵣ·uⱼᵣ` — shape at response × shape at force |
| One row/column is enough | Proven by symmetry of the transfer matrix (reciprocity) |
| FRF = sum of hidden SDOFs | Derived: `hᵢⱼ(jω) = Σᵣ SDOFᵣ` — modal superposition |
| Curvefitting finds f, ζ, shapes | Curvefitting finds POLES + RESIDUES — same thing, math names |

📌 **One line for the chapter:** everything measured (FRF) = poles (where modes
live) + residues (how strongly each mode shows at each point). Learn to read
those two and Ch.3–5 becomeyo "how to measure them cleanly."

✍️ **Warm-up:** write your SDOF equation from memory —
`m·ẍ + c·ẋ + k·x = f(t)`. Every equation in §2.2 is this one wearing a costume;
every equation in §2.3 is a *team* of these, uncoupled by a clever change of
coordinates.

---

## 2.1 Introduction — two models, one truth

Two ways to model dynamics, and Ch.2 is the dictionary between them:

| | 🖥️ FEM (analytical) | 🔨 EMA (experimental) |
|---|---|---|
| Starts from | Assumed M, K distributions (mass/stiffness layout) | Measured force + response → FRFs |
| Gives | Frequencies + mode shapes from the **eigensolution** | f, ζ, shapes from **curvefitting** |
| Strength | Design-stage what-ifs before hardware exists | Ground truth of the real built structure |
| Weakness | Wrong assumptions = wrong modes | Bad measurements = wrong parameters |

📌 **The loop that matters:** build FEM → predict → test → **verify/correct FEM
with modal data** → trusted model. EMA has boomed since the 1980s (cheap
analyzers, MIMO acquisition, better estimators, OMA) — Ch.2 is the theory core
that makes all of it legitimate.

🗣️ *Sofia:* "Nobody pays for theory. They pay for the moment the test proves
the FEM wrong *before* the prototype fails. This chapter is that moment's
operating manual."

---

## 2.2 Basic Modal Analysis Theory — SDOF

### 2.2.1 The equation + its (honest) assumptions

Model: lumped mass `m`, linear spring `k·x`, viscous damper `c·ẋ`:

```
m·ẍ + c·ẋ + k·x = f(t)      (linear, time-invariant, constant coefficients)
```

⚠️ All of Ch.2 assumes **linearity**. Real structures with gaps, friction,
loose joints break this — the book's later chapters teach you to *detect* that
breakdown. For now: linear or nothing works.

Assume exponential trial `x = Xeˢᵗ` for free vibration → **characteristic
equation** → two roots (**poles**). Three damping cases exist; the book (and
your career) lives in **underdamped** `ζ < 1`:

```
poles:  s₁,₂ = −ζωₙ ± j·ωₙ√(1−ζ²) = −ζωₙ ± jωd
ωₙ = √(k/m)            ζ = c/cc            cc = 2mωₙ = 2√(km)
```

📌 **Pole anatomy (tattoo this):** real part `−ζωₙ` = decay rate (damping);
imaginary part `ωd` = ringing frequency. Poles come in **complex-conjugate
pairs**. For light damping (<10%), `ωd ≈ ωₙ`. And `ωₙ` itself doesn't care
about damping at all.

📐 **EX1 — feel the numbers.** `m = 2 kg`, `k = 8000 N/m`, `c = 8 N·s/m`:
`ωₙ = √(8000/2) = 63.2 rad/s → fₙ ≈ 10.1 Hz`; `cc = 2·2·63.2 ≈ 253`;
`ζ = 8/253 ≈ 0.032` (3.2% — typical welded steel!); `ωd ≈ 63.2 rad/s`;
poles at `−2 ± j63.2`. Peak amplification `Q ≈ 1/(2ζ) ≈ 16×`. That "16×" is why
resonance breaks things.

### S-plane: where poles live 🖼️

Plot real (damping, σ-axis) vs imaginary (frequency, jω-axis):
- **Undamped:** poles sit ON the jω axis (eternal sine — never happens, shown for completeness).
- **More damping:** poles march **left**, tracing a **circular arc**; `ωd` shrinks.
- **Critical:** pair collides on the σ-axis. **Overdamped:** splits into two real poles.
- 📌 **Radius from origin to pole = `ωₙ`** (undamped natural frequency). The
  angle from the negative real axis encodes ζ.

🔗 **Memory hook:** the S-plane is a *map*; poles are *cities*. Damping pushes
cities west; stiffness pushes them north. The FRF you measure is just the view
of these cities from the jω highway (§2.2.9).

### Forced response: dynamic amplification + the 90° signature

Drive with `f = F·sin(ωt)`; define frequency ratio `β = ω/ωₙ`. Steady response
lags the force, with normalized amplitude (dynamic ÷ static deflection):

```
X/Xstatic = 1 / √[(1−β²)² + (2ζβ)²]        lag φ: 0° → 90° (at resonance!) → 180°
```

- Light damping → peak sits at `ωd ≈ ωₙ`, height `≈ 1/(2ζ)`.
- 📌 **At resonance the response lags the force by exactly 90°.** That phase
  flip is the most robust resonance detector you own — peaks can lie (noise,
  leakage), 90° rarely does.

### Damping estimators: half-power + log-decrement (know them, then outgrow them)

**Half-power (frequency domain)** 🖼️: on the magnitude peak, find the two
frequencies where amplitude = peak/√2 (−3 dB):
```
ζ ≈ (ω₂ − ω₁) / (2ωₙ) = Δω / (2ωₙ)
```
Wider peak = more damping. On the **imaginary** part the half-power points sit
at half the peak height; same points are the **real-part peaks**; on Nyquist
they sit **90° around the circle** from resonance.

**Log-decrement (time domain)** 🖼️: pluck the structure, watch the ring-down:
```
δ = ln(x₁/x₂) ≈ 2πζ     (small ζ; average over n cycles: δ = ln(x₁/xₙ₊₁)/n)
```

⚠️ **Book's honest verdict (both methods):** historically important, exam-favorite —
but real responses are almost never single-mode, so single-mode tricks mislead.
🧪 The professional answer: **modal parameter estimation** (least-squares fit of
poles+residues over a band). Use half-power/log-dec for sanity checks and
interviews, curvefitters for paychecks. (*Viktor fought for this paragraph.*)

📐 **EX2 — half-power in 10 seconds.** Peak at 100 Hz, half-power points at
99 and 101 Hz: `ζ ≈ (101−99)/(2·100) = 1%`. Q ≈ 50. Lightly damped — handle
leakage with care (Ch.1 §1.4 flashback!).

### Force balance: WHY resonance is a damping-only fight 🖼️

Write the equation as four vectors that must sum to zero: applied `F`, elastic
`Kx`, damping `cωx` (leads elastic by 90°), inertia `mω²x` (180° from elastic).
Three regimes:

| Excitation | Dominant balance | FRF region |
|---|---|---|
| `ω ≪ ωₙ` | `F ≈ Kx` — looks **static** | Stiffness-controlled |
| `ω = ωₙ` | `Kx` and `mω²x` **cancel exactly** — only damping opposes F | Damping-controlled |
| `ω ≫ ωₙ` | `F ≈ mω²x` — mass inertia rules | Mass-controlled |

📌 **At resonance, stiffness and inertia annihilate each other; damping alone
holds the bridge.** That's why the resonance peak measures damping and nothing
else — the deepest single insight of §2.2.

📐 **EX3 — cancellation with numbers.** EX1 system at `ω = ωₙ = 63.2`, `X = 1 mm`:
elastic `KX = 8000·0.001 = 8 N`; inertia `mω²X = 2·4000·0.001 = 8 N` — equal,
opposite, gone. Damping `cωX = 8·63.2·0.001 ≈ 0.5 N` balances the entire applied
force. 8 N vs 0.5 N: see why light damping = giant response?

### Laplace: the transfer function in three costumes

Laplace turns calculus into algebra. Same system, three equivalent outfits —
**no new information, just new convenience** (the book stresses this!):

1. **Polynomial:** `H(s) = 1/(ms² + cs + k)` — direct from the equation.
2. **Pole–zero:** factored with roots exposed — poles = denominator roots.
3. **Partial fraction:** sum of `residue/(s − pole)` terms — the form that
   *screams* "I am ready for modal testing."

Inverse-Laplace the impulse → **impulse response** = decaying complex
exponentials `e^(−ζωₙt)·sin(ωdt)` — the time-domain twin of everything above.

### Residue: the number that carries the shape

The transfer function explodes at its poles (division by zero) — the **residue
theorem** extracts the finite, meaningful strength of each pole. For SDOF it's a
constant; for MDOF (§2.3) residues become the **matrix that carries every mode
shape**. 📌 **Pole + residue = the complete DNA.** From just these two you can
rebuild the transfer surface everywhere AND the FRF at every frequency.

### FRF = a slice of the transfer surface at `s = jω` 🖼️

Picture the transfer function as a tent surface over the S-plane with infinite
spikes over each pole. The FRF is the **slice along the jω axis** — walk that
line with a knife and the cut edge is your measured function. Poles near the
axis (light damping) → tall sharp slices; deep poles → low wide ones.

Three portraits of the same slice:
- **Bode** (magnitude + phase): peak at resonance, phase 90°, total 180° flip.
- **Co-quad** (real + imaginary vs f): **real crosses zero, imaginary peaks** at resonance.
- **Nyquist/Argand** (imag vs real): a near-**circle**; resonance sits opposite
  the origin with zero real part; half-power points 90° around. 🖼️

🧪 *Lena:* "Learn to love Nyquist. A clean circle = clean mode. A potato =
overlapping modes, noise, or nonlinearity telling you to slow down."

### D/F, V/F, A/F: the slope detective kit 🖼️

Measure displacement, velocity, or acceleration over force:

| Name | Symbol | From D/F | Stiffness-region slope | Mass-region slope |
|---|---|---|---|---|
| Dynamic compliance | D/F | — | flat (0) | −2 |
| **Mobility** | V/F | × jω | +1 | −1 |
| **Inertance** | A/F | × (jω)² = −ω² | +2 | flat (0) |

(Inverses exist too: dynamic stiffness, impedance, dynamic mass.)
📌 `A/F = −ω²·(D/F)`: acceleration and displacement are **180° apart**, scaled
by `ω²`. 🧪 **Detective trick:** unlabeled plot? Check the far-left and far-right
slopes — `(0,−2)` = displacement, `(+1,−1)` = velocity, `(+2,0)` = acceleration.
Mix-ups between instruments get caught in seconds.

📐 **EX4 — name that plot.** Low-frequency end rises at +2/decade, high end
flat: that's **A/F (accelerance)** — your everyday hammer+accelerometer FRF.

---

## 2.3 Basic Modal Analysis Theory — MDOF (the main event)

### Coupled equations → matrix form (start with 2DOF)

Two masses, force balance on each: mass-1's equation contains mass-2's motion
and vice versa — **coupled**. In matrix form:

```
[M]{ẍ} + [C]{ẋ} + [K]{x} = {F}
```

📌 Off-diagonal terms in C and K ARE the coupling. All three matrices are
**square, symmetric** — that symmetry is the seed of reciprocity (§2.3.2) and
of Ch.1's "one row/column suffices." Assumes linear, time-invariant, constant
coefficients (same honesty clause as §2.2).

### The eigensolution: frequencies + shapes fall out together

Set damping aside (`C = 0`, or proportional to M and/or K) and solve:

```
([K] − ω²[M]){u} = 0     →     det([K] − λ[M]) = 0,   λ = ω²
```

Conceptually (book's walk-through, worth memorizing):
1. **Determinant** = high-order polynomial → its roots = **eigenvalues**
   (the natural frequencies squared). Small systems: direct solvers (Jacobi,
   Givens, Householder); giant FEMs: iterative solvers chasing only the lowest
   modes (subspace iteration, Lanczos).
2. **Substitute** `λ₁ = ω₁²` back in, solve for `{x₁}` (Crout, Cholesky, LDL…)
   → that vector IS **mode shape 1**. Repeat per frequency.
3. At each solution the book shows **elastic forces = inertial forces**:
   the structure in **dynamic equilibrium**, oscillating about **nodes** with
   equal positive/negative lobes. 🖼️ (Mode 1 blue, mode 2 red — the book's
   colors, kept in our PDF.)

📌 The pair (frequency + vector) = **eigenpair**. Eigenvectors are **linearly
independent** and **orthogonal w.r.t. M and K** — the miracle the whole chapter
rides on.

📐 **EX5 — 2DOF intuition.** Two identical floor masses, three springs. Mode 1:
masses move **together** (in phase, low frequency — middle spring barely
stretches). Mode 2: masses move **opposite** (out of phase, high frequency —
middle spring works hard). Two modes = two independent "dance moves"; every
real motion = a mix of the two. That sentence generalizes to a million DOFs.

### Orthogonality → modal mass & stiffness (the uncoupling keys)

```
{uᵢ}ᵀ[M]{uⱼ} = 0,  {uᵢ}ᵀ[K]{uⱼ} = 0        (i ≠ j)
{uᵢ}ᵀ[M]{uᵢ} = mᵢ   (modal mass),   {uᵢ}ᵀ[K]{uᵢ} = kᵢ   (modal stiffness)
```

Stack eigenvectors as columns → **modal matrix [U]**. Transform coordinates:

```
{x} = [U]{p}     (physical motion = shapes × modal responses)
```

and the coupled monster **diagonalizes** (with proportional damping):

```
mᵢ·p̈ᵢ + cᵢ·ṗᵢ + kᵢ·pᵢ = fᵢ ,   fᵢ = {uᵢ}ᵀ{F}   (modal force: how hard F pushes mode i)
```

📌 **Each mode becomes its own SDOF.** Solve `m` tiny equations (often `m ≪ n` —
a handful of modes describe a million-DOF FEM!), then project back with `[U]`.
🖼️ This "decompose → solve → recombine" round-trip is **modal superposition**,
the most-used algorithm in structural dynamics.

🧪 *Viktor:* "Test engineers live the reverse trip: measure FRFs (physical) →
extract poles/residues (modal) → animate shapes (physical again). Same bridge,
walked backwards."

### Laplace for MDOF: global poles, shape-carrying residues

Transform the matrix equation; with zero initial conditions the homogeneous
part gives the **system matrix [B(s)]** (symmetric, since M/C/K are). It yields
**2n poles** (pairs per mode, `−ζᵣωᵣ ± jωdr`). Then the money equation:

```
[H(s)] = [B(s)]⁻¹ = adj[B(s)] / det[B(s)]
         = [residue matrix A(s)] / characteristic polynomial
```

📌 **Denominator → poles: identical for every FRF** (same roots wherever you
measure) — that's why poles are **global properties**. Numerator → residue
matrix, whose symmetry hands you **reciprocity** and, evaluated at each pole,
vectors proportional to the **mode shapes** — every row AND column is a valid
shape solution. Ch.1's node rule now has a birth certificate: reference at a
node zeroes that mode's residue everywhere in the row/column.

### The FRF summation: two faces of one equation 🖼️

Slice at `s = jω`, term by term:

```
Residue form:   hᵢⱼ(jω) = Σᵣ  Aᵢⱼᵣ / (jω − λᵣ) + conj
Shape form:     hᵢⱼ(jω) = Σᵣ  uᵢᵣ·uⱼᵣ / [mᵣ(ωᵣ² − ω² + j2ζᵣωᵣω)]
```

Read the shape form like a story: each mode contributes its **SDOF amplifier**
(the bracket — pure §2.2!) times **`uᵢᵣ·uⱼᵣ` — output-shape × input-shape
filters**. Weak shape at the hammer point OR at the sensor → that mode barely
appears in that FRF. The summed FRF with its individual modal humps underneath
(our PDF redraws this) is the single image to remember from §2.3.

Response to a sine at any frequency = Σ modal responses (book's 2DOF demo):
**below both modes** → mode 1 dominates; **near mode 2** → mode 2 takes over;
**between** → the hybrid Ch.1 §1.8 warned you about. Same moral, now with
equations.

### Cantilever beam, 3 points: the whole theory on one page 🖼️

3 inputs × 3 outputs = 9 FRFs (magnitude/phase/real/imag). Tour:
- **h₃₃ (drive point, tip):** sum of all modal oscillators; peak–valley
  alternation; decomposed per-mode underneath.
- **h₃₂, h₃₁ (cross):** same poles, different residue weightings — watch one
  mode shrink as the force point nears its node.
- **Roving hammer** (fixed accel) = **row**; **roving accels** (fixed shaker) =
  **column** — Ch.1's table, now derived.
- Read **mode 1 from column 3**: amplitudes ∝ shape values (book's numbers are
  illustrative; ours in the PDF too). Any row/column works; the **waterfall of
  imaginary parts** (tip reference) draws all three shapes in the air.

📐 **EX6 — read a shape from a column.** Mode-1 imaginary peaks down column 3:
`[0.4, 1.1, 2.0]` → normalize by tip: `[0.2, 0.55, 1.0]` — first-bending shape,
zero at root growing to tip. Congratulations: you just did modal parameter
estimation by hand.

### Time–frequency–modal: three doors, one room 🖼️

- **Time:** tip response = Σ damped decaying sines (one per mode).
- **Frequency:** FRF = Σ SDOF oscillators (same modes, jω clothes).
- **Modal:** decoupled SDOF equations + shapes (the engine room).
Convert freely between them; the physics never changes outfits, only you do.

### Turbine-blade superposition: the full computation (2.3.9)

Impulse near the root of a blade (cantilever model), tip response wanted:
eigensolve the FEM → modal mass/damping/stiffness + modal force per mode →
solve 3 trivial SDOF time responses → **project back with shapes** → add.
Plot: total tip response with each mode's contribution visible beneath.
📌 This is every commercial solver's inner loop. The book even links it as an
animation — motion beats equations for gut feeling.

📐 **EX7 — why truncation works.** Blade needs response to 50 Hz; modes at
8, 22, 47, 130, 260 Hz…: keeping 3 modes (`m = 3 ≪ n`) captures the band —
higher modes answer quasi-statically (see: residual terms, §1.7 callback!).

---

## 2.4 Summary — the whole EMA process on one map 🖼️

Follow the book's master schematic (our PDF redraws it as a flowchart):

```
ASSUME      EIGENSOLVE        LAPLACE              SYNTHESIZE
FEM (M,K) → freqs + shapes → [H(s)] = adj/det → poles + residues → FRF anywhere
                                                              ↕  compare!
MEASURE       TRANSFORM          RATIO              CURVEFIT
force+resp → FFT time→freq → H = X/F → extract poles + residues → validate FEM
```

- Forward path (top): assumptions → predictions.
- Backward path (bottom): measurements → parameters — **identical math
  objects** (poles/residues), opposite direction.
- The gap between them = modeling error + measurement error. Your career =
  shrinking both. Next: **Ch.3** (signal processing: sampling, leakage,
  windows — measuring right), **Ch.4** (excitation: hammer/shaker mastery),
  **Ch.5** (parameter estimation: the curvefitting zoo).

---

## 📋 One-page Revision

| # | Big idea | Punchline |
|---|---|---|
| 1 | Pole anatomy | Real = damping (−ζωₙ), imag = frequency (ωd); conjugate pairs |
| 2 | S-plane map | Damping pushes poles west on a circle; radius = ωₙ |
| 3 | Resonance signature | 90° lag; stiffness/inertia cancel; damping alone resists |
| 4 | Damping quickies | ζ ≈ Δω/(2ωₙ); δ = ln(x₁/x₂) ≈ 2πζ; pros use estimators |
| 5 | Transfer = 3 costumes | Polynomial / pole-zero / partial fraction — same info |
| 6 | Residue | Finite strength at a pole; pole + residue = full DNA |
| 7 | FRF = slice | H(jω) = transfer surface cut along the jω axis |
| 8 | Three portraits | Bode (peak+90°) · co-quad (real 0, imag peak) · Nyquist (circle) |
| 9 | Regions | Low-f stiffness · resonance damping · high-f mass |
| 10 | D/V/A slopes | (0,−2) / (+1,−1) / (+2,0) — identify unlabeled plots instantly |
| 11 | Eigensolution | det → freqs → substitute → shapes; dynamic equilibrium + nodes |
| 12 | Uncoupling | {x}=[U]{p}; m tiny SDOFs replace n coupled equations (m≪n) |
| 13 | Global poles | Same denominator everywhere; residues carry shapes + reciprocity |
| 14 | FRF sum | hᵢⱼ = Σ shapeᵢ·shapeⱼ × SDOFᵣ — filters you can read |
| 15 | Full loop | FEM→predict vs test→extract; same poles/residues both ways |

**7 formulas that carry the chapter:**
`ωₙ=√(k/m)` · `s=−ζωₙ±jωd` · `X/Xst=1/√[(1−β²)²+(2ζβ)²]` ·
`ζ≈Δω/2ωₙ` · `([K]−ω²[M]){u}=0` · `{uᵢ}ᵀ[M]{uⱼ}=mᵢδᵢⱼ` ·
`hᵢⱼ=Σᵣuᵢᵣuⱼᵣ/mᵣ(ωᵣ²−ω²+j2ζᵣωᵣω)`

---

## ✍️ Self-test

1. A pole sits at `−3 ± j40`. Give ζ, ωₙ, ωd. Light or heavy damping?
2. Why does the resonance peak measure *damping* and nothing else?
3. Half-power points at 49.5/50.5 Hz, peak 50 Hz. Estimate ζ and Q.
4. Real part zero + imaginary peak at some frequency. What are you looking at?
5. Nyquist plot looks like a potato, not a circle. List 3 suspects.
6. Unlabeled FRF: flat low end, −2 slope high end. Which form? How do you get V/F from it?
7. Why are poles "global" but residues "local"?
8. Reference at a mode's node kills the mode — prove it in one line from the shape-form FRF.
9. A 200k-DOF FEM needs response to 100 Hz; 12 modes live below it. How many equations do you really solve, and what carries the rest?
10. Top path says 88 Hz, test says 82 Hz. Name one modeling-side and one measurement-side suspect.

<details>
<summary><b>Answers</b></summary>

1. ωd=40, ζωₙ=3 → ωₙ=√(40²+3²)≈40.1, ζ≈3/40.1≈7.5% — moderate.
2. At ωₙ elastic/inertial forces cancel exactly; only `cωX` opposes F (§2.2 force balance).
3. ζ≈(50.5−49.5)/(2·50)=1%; Q≈50.
4. Resonance on a co-quad plot (SDOF-like, well-separated mode).
5. Overlapping modes, noise/leakage, nonlinearity (or bad calibration) — slow down and check.
6. D/F (compliance). Multiply by jω.
7. Poles = denominator roots, same for all i,j; residues = numerator, per input–output pair.
8. `uⱼᵣ = 0` at the node → every term `uᵢᵣ·uⱼᵣ = 0` for mode r. QED.
9. 12 modal SDOFs; higher modes folded in quasi-statically via residuals (+truncation error).
10. Modeling: wrong boundary conditions / mass-stiffness distribution. Measurement: mass loading, Nonlinearity, poor calibration, temperature shift.

</details>

---

## 🧪 Theory-to-lab checklist

**Before testing:** ☐ predict band + mode count from FEM/drawings? ☐ reference
off all expected nodes? ☐ A/F or V/F — slope-check first plot?
**During:** ☐ 90° phase at every claimed resonance? ☐ Nyquist circles, not
potatoes? ☐ drive-point alternation intact? ☐ coherence ≈ 1 in band?
**After:** ☐ poles stable across rows/columns (global!)? ☐ shapes orthogonal-ish?
☐ FEM updated and re-compared?

---

## Glossary (Ch.2)

- **Pole** — root of the characteristic equation; `−ζωₙ ± jωd`; damping + frequency in one number.
- **Residue** — pole's finite strength; in MDOF carries shapeᵢ × shapeⱼ.
- **S-plane** — real-vs-imaginary map of poles; jω axis = where FRFs live.
- **Dynamic amplification** — X/Xstatic vs β; peak ≈ 1/(2ζ) = Q.
- **Half-power / log-decrement** — frequency-/time-domain damping quickies.
- **Transfer function H(s)** — response/input in Laplace land; surface over the S-plane.
- **Partial fractions** — H(s) as Σ residue/(s−pole); the test-ready form.
- **Bode / co-quad / Nyquist** — mag-phase / real-imag-vs-f / imag-vs-real portraits.
- **Compliance / mobility / inertance** — D/F, V/F, A/F (inverses: dynamic stiffness, impedance, dynamic mass).
- **Eigenvalue / eigenvector / eigenpair** — ω² / shape / the pair; from det([K]−λ[M])=0.
- **Orthogonality** — shapes decouple M and K; yields modal mass/stiffness.
- **Modal matrix [U]** — shapes as columns; `{x}=[U]{p}` uncouples the system.
- **Modal force** — `{u}ᵀ{F}`: how hard the input pushes each mode.
- **Modal superposition** — solve tiny modal SDOFs, project back, add.
- **System matrix [B(s)]** — s-domain coefficient matrix; symmetric.
- **Global property** — same for all FRFs (poles, frequencies, damping).
- **Mode superposition truncation** — keeping m≪n modes + residual compensation.

## 🏦 Bank 1 — Formula + symbol bank (extended edition)

| # | Formula | Reads as |
|---|---------|----------|
| 1 | `m ẍ + c ẋ + k x = f` | The equation; everything descends from it |
| 2 | `ωₙ=√(k/m)`, `ζ=c/(2√(km))`, `ωd=ωₙ√(1−ζ²)` | Frequency, damping, damped frequency |
| 3 | `p₁,₂ = −ζωₙ ± jωd` | Poles: decay (real) + ring (imag) |
| 4 | `H(s) = (1/m)/((s−p₁)(s−p₂)) = A₁/(s−p₁)+A₂/(s−p₂)` | Three costumes, one function |
| 5 | `A₁ = (1/m)/(p₁−p₂) = 1/(j2mωd)` | Cover-up residue (pure imaginary) |
| 6 | `H(jω) = 1/((k−mω²)+jcω)` | FRF: slice of H(s) at s=jω |
| 7 | `X/Xst = 1/√((1−β²)²+(2ζβ)²)`, `tan φ = 2ζβ/(1−β²)` | Amplification + phase |
| 8 | `β_D=√(1−2ζ²)`, `β_V=1`, `β_A=1/√(1−2ζ²)` | D/V/A peaks sit apart |
| 9 | `Q=1/(2ζ)=ωₙ/Δω`, `δ≈2πζ`, `ζ=δ/√(4π²+δ²)` | Q, bandwidth, log-dec |
| 10 | `V=jωD`, `A=−ω²D` | D/V/A conversion (+90°/×ω each step) |
| 11 | `det([K]−λ[M])=0`, `λ=ω²` | Eigenvalues = squared frequencies |
| 12 | `{u}ₛᵀ[M]{u}ᵣ=0`, `{u}ₛᵀ[K]{u}ᵣ=0` | Orthogonality (distinct freqs) |
| 13 | `mᵣ={φ}ᵀ[M]{φ}`, `kᵣ={φ}ᵀ[K]{φ}`, `ω²=kᵣ/mᵣ` | Modal mass/stiffness |
| 14 | `H(ω)=Σ {u}{u}ᵀ/(kᵣ−ω²mᵣ+jωcᵣ)` | FRF sum (shape face) |
| 15 | `Hᵢⱼ=Σ Aᵢⱼ/(jω−p)+conj` | FRF sum (residue face) |
| 16 | `hᵢⱼ(0)=ΣA/ω²=[K]⁻¹ᵢⱼ` | Static receipt (residues must pay it) |
| 17 | `C=a[M]+b[K]` → `ζᵣ=a/(2ωᵣ)+bωᵣ/2` | Rayleigh damping (U-curve) |
| 18 | `ω²(u)={u}ᵀ[K]{u}/{u}ᵀ[M]{u} ≥ ω₁²` | Rayleigh quotient (upper bound!) |
| 19 | `Δf ≤ (2ζfₙ)/5`, `T=1/Δf` | Resolution rule (theory sizes the test) |
| 20 | `τ=1/(ζωₙ)`, wait 4–5τ | Transient decay before trusting data |

## 🏦 Bank 2 — FAQ + interview rapid-fire (extended edition)

**FAQ round 1 (core):** peak≠fₙ (D below/V at/A above) · ωₙ never moves, only ωd dips ·
negative imag = residue sign, not broken data · ODS≈shape only AT isolated resonance ·
true poles never differ between FRFs · more modes ≠ better · 90°+peak+coherence+repeat =
resonance · scaling: pattern vs level · drive zeros interlace, cross zeros wander ·
complex modes need non-proportional damping.

**FAQ round 2 (deep):** collocation constrains drive zeros; cross numerators are free ·
proportional damping → real residues; general viscous → complex · Rayleigh `bω/2`
overdamps high modes — fit band = trust band · plot Bode mag first, phase to confirm,
Nyquist only for circle fits · mounts avoid resonance (tune low), absorbers plant a
zero ON it · one-line Ch.2: *poles say when, residues say where, shapes say how*.

**Interview rapid-fire (12):** poles = damping+freq roots · residues = shapeᵢ×shapeⱼ
strengths · reciprocity hᵢⱼ=hⱼᵢ · global = poles, local = residues · 90° = resonance ·
ζ from bandwidth/ring-down · peak ≠ fₙ · drive = co-located, valleys alternate ·
truncation + residuals · V/F peaks exactly at ωₙ · real vs complex modes ·
modes = standing waves of the structure.

## 🏦 Bank 3 — Deep-cuts digest (extended edition)

**Core proofs:** orthogonality (`{u}ₛᵀ[M]{u}ᵣ=0` via premultiply-transpose-subtract) ·
FRF sum (expand `X=Uq`, project, solve scalars, recombine) · log-dec (`δ=2πζ/√(1−ζ²)`)
· Q from half-power (`Δβ≈2ζ` → `Q=1/(2ζ)`) · conjugate pairs = one real sine.

**Damping lab:** Rayleigh fit (EX-V: `a=0.124`, `b=0.00324` through 2%@6.18 + 3%@16.18;
extrapolation overdamps: 9.8% at w=60!) · hysteretic `k(1+jη)`, `η≈2ζ`, freq-domain
ONLY · 3 scalings, one residue (EX-X: 0.724 three ways).

**Zeros/synthesis:** anti-resonance derived — EX-M `wz=10.0 rad/s` interlaces 6.18/16.18 ·
synthesis at mode-2 reso: `h₁₂=−0.0020+j0.0285` (negative residue flips phase to +94°) ·
absorber design (EX-AI: 5 kg + 123 kN/m plants a zero at 25 Hz) · transmissibility
(EX-AG: 88% isolation; more damping WORSENS high-f isolation).

**Bode/transients:** asymptotes navigate, exact math docks (EX-AE) · wait 4–5τ
(EX-AF: τ=0.5 s → 2.5 s) · transient trio + beats kill log-dec on close modes ·
Rayleigh quotient bounds from above (EX-AH: 50.0 → 38.46 vs true 38.2).

**Capstone numbers:** poles `−0.124±j6.179`, `−0.485±j16.173` · h₁₁ zeros `±j10.0` ·
5-route static cross-check all = 0.0100 · 34 worked examples EX-A…EX-AI indexed in §Deep-9.

**Resolution bridge → Ch.3:** `Δf ≤ 2ζfₙ/5` (z=1%@100 Hz → Δf≤0.4 Hz, T≥2.5 s) ·
SISO/SIMO/MISO/MIMO map · state-space first-order form · rigid-body modes (free-free,
soft suspension <10% of first flex) · traps wall (rad/s vs Hz, −3 dB from PEAK,
kN/mm×10⁶, coherence ≠ calibration) · study plans (1-day / 1-week / interview / lab).

*Council sign-off: Meera ✔ theory · Viktor ✔ lab · Lena ✔ signals · Arjun ✔ pedagogy ·
Sofia ✔ field — dissent: none outstanding (see council log for the fights).*
