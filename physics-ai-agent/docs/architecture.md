# System Architecture — Physics AI Agent

> Design principle: **the AI reasons about physics; deterministic computational
> tools perform calculations.** The LLM never does critical arithmetic by
> "thinking" when a solver can compute it.

## 1. System architecture

```
 ┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
 │    User     │────▶│  Orchestrator    │────▶│   LLMProvider       │
 │ (CLI / API) │◀────│  (agent/)        │◀────│ (reasoning/explain) │
 └─────────────┘     └────────┬─────────┘     └─────────────────────┘
                              │ tool calls (deterministic)
        ┌─────────────────────┼──────────────────────────────┐
        ▼                     ▼                              ▼
 ┌─────────────┐     ┌──────────────────┐          ┌─────────────────┐
 │ Knowledge   │     │ Physics+Math     │          │ Verification &  │
 │ formulas,   │     │ solvers (solvers/│          │ Explanation     │
 │ constants,  │     │ physics/, maths) │          │ (checks, levels │
 │ concepts    │     └──────────────────┘          │  1-4, modes)    │
 └─────────────┘              │                    └─────────────────┘
                              ▼
                     ┌──────────────────┐
                     │ Units &          │
                     │ Dimensions       │
                     │ (units/)         │
                     └──────────────────┘
```

Layers:

1. **Interaction layer** (`cli.py`, future API/server): parses requests, streams
   the 13-section response, manages explanation level (1–4) and mode
   (guided/direct/teaching/exam/research/engineering).
2. **Agent layer** (`agent/`): orchestrator, domain classifier, reasoning-plan
   builder, assumption manager, error detector, verification, explanation.
3. **Knowledge layer** (`knowledge/` + `data/`): formulas, constants, concepts,
   references. RAG-ready: every item carries topic/subtopic/equation/
   assumptions/source/difficulty/keywords/related.
4. **Computation layer** (`solvers/`, `mathematics/`, `physics/`, `units/`):
   pure deterministic functions. No LLM calls inside. Fully unit-tested.
5. **LLM abstraction** (`llm/`): `LLMProvider` interface with `EchoProvider`
   (offline deterministic) and `OpenAICompatibleProvider` (any OpenAI-style
   API: OpenAI, vLLM, Ollama, LM Studio). Swapping models never touches physics.
6. **Visualization** (`visualization/`): Matplotlib plots saved to files
   (time histories, FRF/Bode, FFT spectra, sweeps). Only generated on request
   or when they materially aid understanding.

## 2. Repository structure

```
physics-ai-agent/
├── README.md  pyproject.toml  requirements.txt  .env.example
├── docs/                  architecture.md  physics-methodology.md  contribution-guide.md
├── src/physics_agent/
│   ├── config.py  cli.py
│   ├── agent/             orchestrator, classifier, reasoning, explanation,
│   │                      verification, modes
│   ├── physics/           base + mechanics, vibrations, thermo, fluids,
│   │                      electromagnetism, optics_waves, quantum, relativity,
│   │                      dimensionless  (+ registry for new domains)
│   ├── mathematics/       numerical_methods, differential_equations
│   ├── units/             converter, dimensional_analysis
│   ├── knowledge/         formulas, constants, concepts
│   ├── solvers/           symbolic, numerical, ode, eigenvalue, spectral
│   ├── visualization/     plots
│   ├── llm/               base, echo, openai_compatible
│   └── tools/             registry (all callable tools)
├── data/
│   ├── formulas/          mechanics, vibrations, thermo_fluids, em_optics, modern (.json)
│   ├── constants/         codata2022 subset (.json)
│   ├── examples/  knowledge/
├── tests/  (mirror of src: units, physics, mathematics, agent)
└── examples/  basic/  engineering/  vibrations/  advanced/
```

## 3. Agent architecture (15 components → modules)

| # | Spec component              | Implementation                          |
|---|-----------------------------|-----------------------------------------|
| 1 | Problem Understanding Agent | `agent/reasoning.py:parse_problem`      |
| 2 | Physics Domain Classifier   | `agent/classifier.py`                   |
| 3 | Knowledge Retrieval Agent   | `knowledge/formulas.py`, `concepts.py`  |
| 4 | Equation Selection Agent    | `agent/reasoning.py:build_plan`         |
| 5 | Mathematical Reasoning Eng. | `agent/reasoning.py` + `solvers/`       |
| 6 | Symbolic Solver             | `solvers/symbolic.py`                   |
| 7 | Numerical Solver            | `solvers/numerical.py`, `ode.py`, ...   |
| 8 | Unit Conversion Engine      | `units/converter.py`                    |
| 9 | Dimensional Analysis Engine | `units/dimensional_analysis.py`         |
| 10 | Verification Agent          | `agent/verification.py`                 |
| 11 | Visualization Agent         | `visualization/plots.py`                |
| 12 | Explanation Agent           | `agent/explanation.py`, `modes.py`      |
| 13 | Error Detection Agent       | `agent/verification.py:detect_errors`   |
| 14 | Assumption Manager          | `agent/reasoning.py:Assumption`         |
| 15 | Reference Manager           | `knowledge/concepts.py`, formula sources|
| + | Coordinator/Orchestrator    | `agent/orchestrator.py`                 |

New physics domains plug in via `physics/base.py:DomainModule` and
`physics/__init__.py:register_domain` — no orchestrator changes needed.

## 4. Data model

**Formula** (`data/formulas/*.json`, schema in `knowledge/formulas.py`):

```json
{
  "name": "Newton's Second Law",
  "equation": "F = m*a",
  "domain": "classical_mechanics",
  "variables": {"F": {"meaning": "Force", "si_unit": "N"},
                "m": {"meaning": "Mass", "si_unit": "kg"},
                "a": {"meaning": "Acceleration", "si_unit": "m/s^2"}},
  "assumptions": ["classical regime", "inertial frame"],
  "validity": "v << c",
  "derivation": "concepts:newton_laws",
  "related": ["momentum", "impulse"],
  "mistakes": ["mixing mass and weight"],
  "applications": ["dynamics of particles"],
  "difficulty": 1,
  "keywords": ["force", "mass", "acceleration"],
  "source": "standard undergraduate mechanics"
}
```

**Constant** (`data/constants/*.json`): `{symbol, name, value, unit, description,
source, precision}`. SI values, never hard-coded in solvers.

**Dimension**: 7-vector over SI bases `[M, L, T, I, Θ, N, J]`; derived units
resolve to base vectors for consistency checks.

**Plan** (`agent/reasoning.py:SolutionPlan`): parsed quantities, candidate
equations, tool calls with arguments, verification checklist state, KNOWN /
ASSUMED / DERIVED / ESTIMATED / UNKNOWN ledger.

**Result** (`physics/base.py:PhysicsResult`): value(s), SI unit, symbolic form,
method, assumptions, verification notes, provenance tag (one of GENERAL
PHYSICS KNOWLEDGE / USER-PROVIDED / EXTERNAL REFERENCE / COMPUTED /
ASSUMPTION).

## 5. Tool architecture

`tools/registry.py` exposes a uniform `Tool(name, description, parameters,
function)` table; the orchestrator (or an LLM with function calling) selects
tools dynamically:

`solve_equation`, `convert_units`, `check_dimensions`, `derivative`,
`integral`, `solve_ode`, `solve_eigenvalue_problem`, `fft`, `plot_function`,
`parameter_sweep`, `sensitivity_analysis`, `verify_solution`,
`lookup_formula`, `lookup_constant`.

Each tool is a thin, typed wrapper over the computation layer, so results are
reproducible and testable without any LLM.

## 6. Execution flow (the 10-step workflow → code)

1. `parse_problem` — extract knowns/unknowns/units/system.
2. `classify` — domain, sub-domain, problem type, complexity, methods.
3. `build_plan` — physical model slots (geometry, coords, forces, BCs, ...).
4. Principle/equation selection — from formula DB + reasoning rules.
5. Derivation — symbolic path first (`solvers/symbolic.py`).
6. Dimensional/unit check — `units/` gates every numeric step.
7. Symbolic rearrangement → substitution.
8. Numeric computation — via tools only.
9. `verification.py` — dimensional, limiting-case, magnitude, conservation,
   analytic-vs-numeric, plausibility checks; `detect_errors` scans inputs.
10. `explanation.py` — physical meaning at the requested level/mode.

Simple questions collapse steps 3–5/9–10 automatically (see
`orchestrator.py:COMPLEXITY` handling); research questions expand derivation.

## 7. Technology choices

| Concern           | Choice (+ rationale)                                   |
|-------------------|--------------------------------------------------------|
| Language          | Python 3.10+ (scientific ecosystem)                    |
| Arrays/linear alg | NumPy; eigen/sparse via SciPy                          |
| ODE/roots/opt/fit | SciPy (`solve_ivp`, `root_scalar`, `quad`, `curve_fit`)|
| Symbolic          | SymPy (derivation, rearrangement, exact checks)        |
| Plotting          | Matplotlib (Agg backend; file output, no GUI needed)   |
| Tables/sweeps     | pandas (parameter sweeps, sensitivity tables)          |
| Data files        | JSON (+ YAML support) — human-editable, RAG-ready      |
| LLM access        | stdlib `urllib` OpenAI-compatible client (zero new dep)|
| Tests             | pytest; deterministic seeds; tolerance-based asserts   |
| Packaging         | setuptools `src/` layout, `physics-agent` CLI entry    |

No commercial FEA dependency: the FEA module (`physics/` + knowledge notes)
teaches concepts (convergence, singularities, prestress, contact) and solves
textbook-scale FEM examples (1-D/2-D reference implementations live in
`mathematics/` + examples) rather than replacing ANSYS/Abaqus.

## 8. Implementation roadmap

- **v0.1 (this release)**: foundation — units/dimensions, constants/formulas
  DBs, classifier, orchestrator, symbolic/numeric/ODE/eigen/FFT solvers,
  mechanics/vibrations/thermo/fluids/EM/optics/quantum/relativity core
  solvers, verification, explanation levels/modes, Echo + OpenAI-compatible
  LLMs, CLI, tests, examples, docs.
- **v0.2**: persistent RAG store (embeddings + vector index over `data/`),
  FBD diagram generator, uncertainty propagation (Monte Carlo), 1-D FEM
  reference solver, control-systems module (transfer functions, Bode margins).
- **v0.3**: continuum/solid-mechanics tensors, modal-analysis pipeline,
  rotor-dynamics (Campbell, critical speeds), acoustics, statistics-mechanics
  ensembles, PDE demo solvers (heat/wave, method-of-lines).
- **v0.4**: multiphysics coupling patterns (FSI/thrmo-mechanical), fatigue
  (S–N, Miner), optimization-based inverse problems, web/API server.
