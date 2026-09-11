# 📓 Chapter 1 — Introduction to Experimental Modal Analysis
### *A Simple Non-mathematical Presentation* (detailed notes + extras)

> **Book:** *Modal Testing: A Practitioner's Guide* · **Chapter 1 ( §§1.1–1.9 )**
> **Reader:** recent MechE grad, basic vibrations (SDOF) · **Style:** handwritten-like —
> read top to bottom like a friend's best notebook.
> **Council verdict:** ✅ shipped (log: `chapter-01-council-log.md`)

**Legend used in these notes:**
📌 key idea · 🧪 lab tip · ⚠️ exam/lab trap · 🔗 bridge to basics you know ·
✍️ try-it-yourself · 🗣️ council voice

---

## §0 Primer — what you already know → what this chapter adds 🔗

You know the **SDOF spring–mass–damper**:

```
m·ẍ + c·ẋ + k·x = f(t)        natural frequency  fn = (1/2π)·√(k/m)
```

| You already know (SDOF) | This chapter adds (real structures) |
|---|---|
| 1 natural frequency | **Many** natural frequencies (one per mode) |
| Resonance = big response near fn | Each mode resonates **in its own shape** |
| Damping ratio ζ controls peak height/width | Every mode has **its own damping** |
| FRF of 1 oscillator: 1 peak | FRF of a structure: **many peaks** = many oscillators hiding inside |
| Time response tells the story | Time trace is messy → **frequency domain (FFT)** tells the story |

📌 **One-line mental model for the whole chapter:** a real structure behaves
like a *team of SDOF oscillators* glued together. Modal analysis = identifying
each team member (its frequency, damping, shape). Everything else in Ch.1 is
"how do we see them clearly in measurements."

✍️ **Warm-up:** hum near a steel thali/plate and hear it ring at certain
pitches — those preferred pitches are its natural frequencies. Tapping different
spots excites them differently. That is the entire plate experiment of §1.1,
in your kitchen.

---

## 1.1 Could you explain modal analysis to me?

### The 3-step engineering logic (cantilever beam story)

1. **Characteristics** (length, E, I, density…) describe the beam — but alone
   they can't tell you deflection, stress, or pass/fail.
2. **+ Loads** → you can compute response (deflection/stress/strain).
3. **+ Design spec** (allowable values) → only now can you judge good/bad.

📌 **Modal analysis gives step-1-type data for dynamics:** natural frequency,
damping, mode shape for each mode. Powerful — but ⚠️ **by itself it cannot
say "this design passes"**, because that needs loads + spec too. (In real
troubleshooting, loads/specs are often unknown — that's exactly when modal
thinking saves you.)

### Structural dynamics vs modal analysis (computer-cabinet story)

- **Structural dynamics** = the full movie: all inputs (fan, disk drive,
  external bumps) → total response. Time traces look like chaos.
- **Modal analysis** = the cast list: the system's own modes. In the
  **frequency domain** the chaos separates into clear peaks — and those peaks
  sit at the **modes**. So modal data explains *why* the response movie looks
  the way it does.

📌 Think: **modes = band-pass filters.** Each mode amplifies input energy near
its own frequency and ignores the rest; the measured response = sum of all
modal filters × input spectrum. Uneven input spectrum → uneven peak heights
(even tall modes can look small if starved of input energy there).

### The plate experiment (the heart of §1.1)

Setup: free plate, sinusoidal force of **constant peak, varying frequency**
at one corner, accelerometer at another corner.

1. **Sine sweep in time:** response amplitude breathes up and down as the
   excitation frequency slides — same force, wildly different response.
   Maxima = you're crossing a **resonance**.
2. **FFT → FRF:** the frequency response function shows **4 clean peaks**
   (this plate, this bandwidth). Overlay time-sweep maxima on FRF peaks —
   they line up. ⚠️ A *random* time trace would be unreadable; the FRF rescues us.
3. **Dwell at each peak with 45 accelerometers:** freeze the excitation at one
   natural frequency and map the deformation everywhere:
   - Mode 1 → 1st bending · Mode 2 → 1st torsion/twist ·
     Mode 3 → 2nd bending · Mode 4 → 2nd torsion.
   - 🗣️ *Meera:* "Strictly speaking these operating deflections are only
     *approximately* the mode shapes (neighbors always leak in a little) —
     but for well-separated modes the approximation is excellent, so the book
     calls them mode shapes here."

📌 **Mass and stiffness place the modes; damping sizes the peaks.**
Design engineers use modes to *avoid* resonances; test engineers use them to
*diagnose* noise/vibration failures.

### Two analogies from the book, retold (learn these — interview gold)

**🍲 Cookbook (Example 1).** A cookbook has hundreds of ingredients, but each
recipe uses a small subset in its own proportions. Likewise a structure has
many modes, but each loading uses its own subset — low-frequency loading wakes
low modes, impacts wake broad sets. Change the loading → change the "recipe".

**🎻 100-piece orchestra (Example 2).** Each score uses different instruments
at different intensities; one out-of-tune player ruins the piece, and you can
only find the culprit by listening to players *individually*. Same with
structures: total response won't tell you the faulty contributor — **modes
let you audition each player separately.** That's modal analysis's superpower.

### 🗣️ Council-added analogy (Arjun, for never forgetting)

**🛝 Playground swings:** pushing at random times = weak, chaotic motion
(broadband input, messy time trace). Pushing *in rhythm* = giant amplitude
(dwell at resonance). Two swings tied with a rope = coupled modes (bend + twist
of the plate!). Every "trick" in Ch.1 is a fancier version of finding the
rhythm.

✍️ **Try it:** tap a ruler clamped to a table (cantilever!) at different
overhang lengths — pitch drops as overhang grows (k falls). You just did
"mass and stiffness place the modes" with stationery.

---

## 1.2 Just what are these measurements called FRFs?

📌 **FRF = output ÷ input, in the frequency domain.**
Measure force AND response simultaneously (response = displacement, velocity,
or acceleration) → FFT both → divide. Result is **complex**:
magnitude + phase ⟺ real + imaginary. All four views show the same truth.

### The 3-DOF beam → the 3×3 FRF matrix (Example)

3 push points × 3 measure points = **9 FRFs**, written `h_out,in`
(matrix row = response point, column = force point):

```
              force @ 1   force @ 2   force @ 3
response @ 1 [   h11         h12         h13   ]
response @ 2 [   h21         h22         h23   ]
response @ 3 [   h31         h32         h33   ]   ← "reference 3" row
```

**Drive-point FRF** (`h33`: push and measure at the *same* point) has 3 famous
signatures — memorize like a phone number:

| # | Drive-point signature | Why it matters |
|---|---|---|
| 1 | Peaks (resonances) and valleys (anti-resonances) **alternate** | Your #1 data-quality check |
| 2 | Phase **drops 180°** over a resonance, **gains 180°** over an anti-resonance | Confirms peak vs valley |
| 3 | All **imaginary-part peaks point the same way** | Quick visual sanity check |

🧪 *Viktor:* "First thing I check on any drive-point plot: alternate peak–valley–peak?
Imag peaks all same direction? If not, suspect the measurement, not the theory."

### Reciprocity → you don't need all 9 FRFs

Because the M, C, K matrices are symmetric, **`hij = hji`** (push at i/measure
at j = push at j/measure at i). So **one row OR one column** of the matrix is
enough to get all mode shapes. (The book's 15-point waterfall plot shows the
same idea at higher resolution — peaks of the imaginary part trace each shape.)

### 1.2.1 Why is only one row or column needed? (+ the NODE rule)

- Read the **imaginary-peak heights** across one row → the shape pops out
  (row 3 and row 2 both show mode 1; heights differ by a scale factor — the
  *shape* is what matters).
- ⚠️ **TRAP — the node rule:** with the reference at point 2, **mode 2
  vanishes** — point 2 sits on mode 2's node (zero-motion line).
  📌 **Never put your reference on (or near) a node of a mode you need.**
  Later chapters turn this into reference-selection strategy.

✍️ **Micro-example:** imaginary peaks across 3 points read `[+0.2, +0.9, +1.6]`
→ first-bending shape (all same sign, growing). If they read `[+1.0, 0.0, −1.0]` →
second-mode-ish shape with a node at the middle — and a warning that a
reference *at* the middle would miss this mode entirely.

---

## 1.3 What's the difference between a shaker test and an impact test?

### Theory: none. Practice: plenty.

| | 🔨 Roving-hammer (impact) | 📳 Shaker |
|---|---|---|
| You get | One **ROW** (response reference fixed, hammer roves) | One **COLUMN** (force reference fixed, accelerometers rove) |
| Best at | Fast, portable, no attached hardware | Controlled input, better for big/heavy/damped structures |
| Main enemies | Tip choice, double hits, leakage (see §1.4) | Mass loading, stinger effects (see below) |

📌 **The test article = structure + everything touching it:** suspension,
cables, accelerometer masses, shaker + stinger. Theory assumes massless sensors
and perfect forces — the lab does not.

**Two classic shaker gotchas:**
1. **Roving-mass effect** — one accelerometer is nothing vs the whole machine,
   but huge vs a thin panel's local mass. Moving sensors between readings
   *retunes* the structure mid-test. 🧪 Fixes: leave all accelerometers mounted
   (use a few at a time), or add **dummy masses** at unmeasured points.
2. **Shaker/stinger stiffness + mass** — the stinger's job is to *decouple*
   shaker dynamics from the structure (push purely axially), but residual
   effects often survive. Impact tests dodge this entirely — hence hammer-vs-shaker
   differences on the same structure.

### 1.3.1 What do we actually measure to compute the FRF? (the analyzer chain)

```
sensor → anti-alias filter → ADC → window → FFT → avg spectra → FRF + coherence
```

| Stage | What happens | Enemy |
|---|---|---|
| Transducers | Force cell + accel/vel/disp pickup | Bad mounting, saturation/overload |
| **Anti-alias filter** (analog) | Kills energy above ½ sample rate | ⚠️ **Aliasing**: high-f energy folds back and corrupts the band — the reason good analyzers cost more (phase-matched filters) |
| **ADC** (12/16/24-bit) | Digitizes the waveform | **Sampling** (time/freq resolution) + **quantization** (amplitude steps) errors |
| **Window** | Weights the record so FFT's periodicity demand is ~met | Leakage if skipped wrongly (below) |
| **FFT → linear spectra → averaged power/cross spectra** | Input auto-spectrum, output auto-spectrum, cross-spectrum | Noise (averaging fights it) |
| **FRF + coherence** | FRF = cross/input (essentially); **coherence 0–1 = "how much of the output came from the measured input"** | Coherence ≪ 1 → don't trust that band |

📌 **LEAKAGE (the #1 villain of Ch.1):** the FFT assumes your record either
covers all time or **repeats forever**. A cut-off sine violates that → energy
*leaks/smears* across frequencies. Fix = **windows** (weighting functions that
taper the record so it *looks* periodic). Windows distort a little; leakage
distorts catastrophically. (§§1.4–1.6 = the war against leakage.)

🗣️ *Lena's one-liner:* "Sample rate picks your map's borders, bits pick its
resolution, windows pick your poison — leakage or taper. Choose taper."

---

## 1.4 What's the most important thing when impact testing? 🔨

Only two headline items here (full war stories in Ch.7):

### (a) Hammer-tip hardness = your frequency-range knob

- **Harder tip → wider excited band** (short sharp pulse); **softer tip →
  narrower band** (long gentle push). General rule with exceptions — verify on screen.
- 🧪 **What good looks like:** flat-ish input spectrum + coherence ≈ 1 across
  the band of interest. **What bad looks like:** spectrum rolling off + coherence
  + FRF dying in the upper half (you simply didn't feed those modes any energy).
- ⚠️ Soft tip isn't "wrong" — it's wrong only if you needed the higher modes.
  If your band of interest is the flat part, ship it.

### (b) The response must die before the record ends (else: exponential window)

Lightly damped structures keep ringing past the sample interval → leakage.
Standard rescue = **exponential window** on the response (artificially decays
the tail to ~zero). But:

📌 **Windows damage data — always try the cures first:**
1. **Narrower frequency span** (= longer time record), and/or
2. **More spectral lines** (= finer resolution = longer record) —
   both give the vibration more time to decay naturally.

🧪 *Viktor's pre-flight:* "Tip? Decay? Coherence? — three glances before I
believe any hammer FRF." (Plus: no **double hits**, hit squarely, watch for
**filter ring** and saturated-but-not-overloaded sensors — Ch.7 previews.)

---

## 1.5 What's the most important thing when shaker testing? 📳

📌 **Pick an excitation that needs no window.** Everything else is details (Ch.8).

| Excitation | Leakage? | Window? | Notes |
|---|---|---|---|
| **Burst random** | ✅ leakage-free (whole transient + decay captured in ONE record) | **None** | Workhorse of modern modal testing |
| **Sine chirp** (swept sine) | ✅ leakage-free (signal repeats exactly in the record) | **None** | Great control of the band |
| Plain **random** | ❌ leaks (never periodic in the window) | Hanning (mandatory) — and **still slightly distorted** | Easy to run, worst data of the three |

🗣️ *Lena:* "Random+Hanning is the fast food of excitation: convenient,
satisfying, slightly guilty. Burst random and chirp are home cooking."

✍️ **Memory hook:** **B**urst and **C**hirp = **B**ye-**C**iao windows.
(**B**urst fits the **B**ox; **C**hirp **C**ycles exactly.)

---

## 1.6 Tell me more about windows — they seem pretty important! 🪟

They are. Motto: **no window if you can avoid it; the right window if you can't**
(field data and operating measurements often give you no choice).

| Window | Shape in words | Use it when… | Typical pairing |
|---|---|---|---|
| **Uniform** (rectangular/boxcar/"no window") | Gain = 1 everywhere | Signal fully captured in one record **or** guaranteed periodic-in-window | Impact (both pulse + decay fit) · burst random · chirp · pseudo-random · stepped sine |
| **Hanning** | Bell/cosine, ends → 0 | Signal won't satisfy periodicity (random/field data) | Shaker random, operating data |
| **Flat-top** | Broad flat crown | Pure sine of unknown period; amplitude accuracy matters | Calibration, constant-speed (RPM) excitation |
| **Force** | 1 only around the hammer pulse, 0 elsewhere | Impact force channel (kills noise between hits) | Always with… |
| **Exponential** | Decaying curve | Impact response still ringing at record end | …the force window, as a pair |

⚠️ **Price of every window:** peak amplitudes get less accurate and the
structure **looks more damped than it is**. Acceptable — leakage's smearing is
far worse. (Deep math in the signal-processing chapter.)

✍️ **One-question drill:** "Burst random test — which window?" → *Uniform/none.*
"Factory-floor random vibration?" → *Hanning.* "Hammer test, response ringing
past the record?" → *Force + exponential.* "Calibrating with a sine?" → *Flat-top.*

---

## 1.7 So how do we get mode shapes from the plate FRFs?

### Step 1 — peak-picking (the simple, honest start)

6 points → 6×6 = **36 possible FRFs**. Read the **imaginary-part peaks** mode by mode:

- **Mode 1 (bending):** points 1,2,5,6 ≈ −1; points 3,4 ≈ +1 → classic first-bending
  arc (all 45 points confirm it).
- **Mode 2 (torsion):** 1:+2, 2:−2, 5:−2, 6:+2, and **3,4 ≈ 0** → twist with a
  **node line through 3–4**. (Hello again, node rule from §1.2.1.)

### Step 2 — curvefitting (what software really does)

Peak-picking is fine for simple, well-separated modes. Production work uses
**modal parameter estimation = curvefitting**: decompose the measured FRF into a
**sum of SDOF oscillators** (see §0's mental model — here it becomes literal):

```
measured FRF  =  SDOF(mode 1) + SDOF(mode 2) + SDOF(mode 3) + … + residuals
```

**The analyst's three inputs** (your job; the algorithm does the rest):
1. **Frequency band** to fit (fit in bands, a few modes at a time);
2. **How many modes** live in that band (hard when modes crowd — indicator
   tools help; full toolbox in Ch.5/Ch.9);
3. **Residual terms** — compensation for modes *outside* the band still tugging
   on it.

⚠️ Garbage in, garbage out: curvefitting cannot rescue bad FRFs — which is why
§§1.3–1.6 (measurement quality) come *before* estimation in a practitioner's
head. 🗣️ *Sofia:* "I've never seen a curvefitter fix a double-hit. I've seen
many analysts try."

---

## 1.8 Modal data and operating data (don't mix these up!)

### 1.8.1 What is operating data?

**Operating data = response ONLY.** The machine runs (forces unknown/unmeasured),
you record vibration. Recall the golden chain:

```
response  =  FRF (system filter)  ×  force (whatever it is)
```

- The FRF/modes decide *how* the structure wants to move; the operating force
  decides *which* modes get to play and how loudly.
- Plate demo with a single-sine force at one corner (2 modes for simplicity):
  - **Excite near mode 1** → operating deflection shape **≈ mode 1** (+ a whisper of mode 2).
  - **Excite near mode 2** → shape **≈ mode 2** (+ a whisper of mode 1).
  - **Excite midway** → a strange hybrid nobody recognizes — until you decompose
    it: a little bending + a little torsion. **Operating shapes are linear
    combinations of mode shapes.** With broadband force, many modes join the sum.
- ⚠️ With operating data you never measure the force or the FRF — so you can't
  see *why* the shape looks that way. That's the whole argument for modal testing.

### 1.8.2 So what good is modal data? (the payoff slide)

| Superpower | What it means | Needs |
|---|---|---|
| **SDM — structural dynamic modification** | Predict "what if we add ribs/mass/damping *here*?" **without cutting metal** | Modal model (f, ζ, shapes) |
| **Forced-response simulation** | Predict response to *any* hypothetical force | Modal model |
| **FEM correlation & updating** | Check/fix the finite-element model against reality | Modal model + FEM |

📌 Modal data = the reusable *model* of the system. Operating data = a *snapshot*
of one situation.

### 1.8.3 Should I collect modal or operating data? (the manager's question)

**Both, whenever schedule and budget allow.** If forced to choose, know what you lose:

| | Modal data | Operating data |
|---|---|---|
| Measures | Force **and** response → FRF → true f, ζ, shapes | Response only |
| Gives | System characteristics; SDM + simulation + FEM correlation | True in-service behavior |
| Can't | Say pass/fail alone (needs loads + spec — §1.1's lesson!) | Be used for SDM/simulation; shapes often confusing |
| Collect when | Designing, modifying, validating models | Machine is running and you need ground truth |

🗣️ *Sofia's field rule:* "Operating data tells you **where it hurts**; modal data
tells you **why, and what to change**. Painkillers or cure — your call."

**Mini-case (Sofia):** a car cabin drones at 2800 RPM. Operating test shows a
hot floor panel — but which fix: stiffen, add damping, or move the exhaust hanger?
Modal test reveals a floor bending mode exactly at that RPM's firing frequency
with a belly at the hot spot → targeted rib + damping patch. Operating found the
pain; modal prescribed the cure.

---

## 1.9 Closing remarks → where the book goes next

Ch.1 gave you the **non-mathematical intuition**: modes as filters, FRFs as the
measurement, hammer vs shaker, leakage vs windows, peak-pick → curvefit, modal
vs operating. Next:

- **Ch.2** — the math under the intuition (SDOF → MDOF theory).
- **Ch.3–5** — signal processing, excitation details, parameter estimation.
- **Ch.6+** — the practitioner's craft: setups, hammer/shaker mastery, case studies.

🔗 **Your study loop from here:** for every later equation, ask "which Ch.1
picture does this formalize?" — if you can answer, you own the chapter.

---

## 📋 One-page Revision (cover the right column, recall, check)

| # | Big idea | Punchline |
|---|---|---|
| 1 | Modal analysis finds… | f, ζ, and shape per mode — the system's dynamic fingerprint |
| 2 | …but can't judge alone | Needs loads + spec (cantilever lesson) |
| 3 | FRF | Output ÷ input in freq domain; complex (mag/phase = real/imag) |
| 4 | Drive point h_ii | Alternating peak/valley · ∓180° phase flips · imag peaks same direction |
| 5 | Reciprocity | hij = hji → one row OR column suffices |
| 6 | Node rule | Reference on a node ⇒ mode invisible — never do that |
| 7 | Shaker vs hammer | Theory same; practice differs (mass loading, stinger, suspension) |
| 8 | FRF chain | Sense → anti-alias → ADC → window → FFT → avg spectra → FRF + coherence |
| 9 | Leakage | FFT demands periodicity; violation smears everything; windows are the tax |
| 10 | Hammer: tip = band knob | Hard = wide; soft = narrow; flat spectrum + coherence≈1 = good |
| 11 | Hammer: ringing tail? | Exponential window — or longer record (narrower span / more lines) |
| 12 | Shaker: best inputs | Burst random & sine chirp = window-free; plain random+Hanning leaks a bit |
| 13 | Windows | Uniform (fits/periodic) · Hanning (random/field) · Flat-top (sine/cal) · Force+Exp (hammer) |
| 14 | Curvefitting | FRF = Σ SDOFs + residuals; analyst sets band, #modes, residuals |
| 15 | Operating vs modal | ODS = Σ modes×force (response only); modal = reusable model (SDM/FEM/sim) |

**5 formulas that carry the chapter:**
`fn=(1/2π)√(k/m)` · `H(f)=X(f)/F(f)` · `hij=hji` ·
`response = FRF × force` · `coherence ≈ 1 ⟺ trustworthy band`

---

## ✍️ Self-test (answers below — no peeking!)

1. Why can't modal data alone say a design is acceptable?
2. Same peak force, swept frequency → response varies wildly. Why?
3. FRF shows 4 peaks but the time trace is chaos. Which do you trust for natural frequencies, and why?
4. Name the 3 drive-point signatures.
5. Your reference accelerometer sits on a mode's node. What happens? Fix?
6. Roving hammer gives a ___ of the FRF matrix; shaker gives a ___.
7. Hammer spectrum rolls off and coherence dies above 800 Hz. Diagnose + fix.
8. Which two shaker excitations need no window, and why is each leakage-free?
9. Burst random / factory random / ringing hammer response / sine calibration → pick windows.
10. ODS at 55 Hz looks like nothing you've seen; modes are at 50 and 60 Hz. Explain.

<details>
<summary><b>Answers</b></summary>

1. Modes are characteristics only; response needs loads, verdict needs spec (§1.1).
2. You're crossing resonances — each mode amplifies input near its own frequency (modal filtering).
3. The FRF — FFT separates the modal filters; time superposition hides them.
4. Peak/valley alternation; −180° at resonance / +180° at anti-resonance; imag peaks all same direction.
5. That mode vanishes from all FRFs. Move the reference off the node.
6. Row; column (fixed response ref vs fixed force ref).
7. Tip too soft → no energy up high. Use a harder tip (verify flat spectrum + coherence≈1); if only <800 Hz matters, it's fine.
8. Burst random (whole transient+decay in one record) and sine chirp (exactly periodic in the record).
9. Uniform/none; Hanning; force+exponential; flat-top.
10. 55 Hz sits between modes → ODS = combination of both (mostly), not a pure mode shape.

</details>

---

## 🧪 Lab checklist (tear-off strip)

**Before:** ☐ band of interest? ☐ tip/excitation picked for that band? ☐ reference
off all nodes? ☐ all sensors mounted (no roving-mass surprise)? ☐ stinger aligned (shaker)?
**During:** ☐ no double hits / square impacts? ☐ response decayed in-record (or windowed)?
☐ no overload/saturation? ☐ coherence ≈ 1 in band?
**After:** ☐ drive-point checks pass? ☐ reciprocity spot-check (hij≈hji)? ☐ logbook filled (tip, span, lines, windows, averages)?

---

## Glossary (first-use definitions, Ch.1)

- **Mode** — one natural pattern: frequency + damping + shape. **Natural frequency** —
  where the mode amplifies most. **Mode shape** — the pattern (vector of relative
  amplitudes/phases). **Damping** — energy loss per cycle; sets peak width/height.
- **FRF** — complex output/input vs frequency. **Drive point** — FRF with force and
  response at the same DOF. **Cross FRF** — different DOFs. **Anti-resonance** — valley
  between peaks (drive-point). **Reciprocity** — hij=hji. **Node** — zero-motion line/point
  of a mode. **Reference** — the fixed DOF of a row/column survey.
- **FFT** — time→frequency transform. **Leakage** — smearing when the record isn't
  periodic-in-window. **Window** — taper weighting to fake periodicity. **Aliasing** —
  high-frequency fold-back from bad sampling/filtering. **ADC/quantization** — digitizer;
  bit depth sets amplitude resolution. **(Auto/cross) spectrum** — averaged building blocks
  of FRF/coherence. **Coherence** — 0–1 data-quality meter.
- **Burst random / sine chirp / random** — shaker signals (§1.5). **Peak-picking** —
  reading shapes from imag-peak heights. **Curvefitting (modal parameter estimation)** —
  decomposing FRFs into SDOF contributions (+residuals). **Residual** — out-of-band modes'
  leftover influence. **ODS (operating deflection shape)** — response-only shape at one
  frequency. **SDM** — predicting design changes from the modal model. **FEM correlation** —
  validating/updating simulation with modal test data.

*Council sign-off: Meera ✔ theory · Viktor ✔ lab · Lena ✔ signals · Arjun ✔ pedagogy ·
Sofia ✔ field — dissent: none outstanding (see council log for the fights we had).*
