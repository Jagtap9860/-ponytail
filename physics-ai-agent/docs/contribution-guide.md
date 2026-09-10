# Contribution Guide

## Adding a physics domain

1. Create `src/physics_agent/physics/<domain>.py` with pure functions
   returning `PhysicsResult` (see `physics/base.py`), SI in / SI out.
2. Register it in `src/physics_agent/physics/__init__.py` via
   `register_domain(...)` with keywords for the classifier.
3. Add formulas to `data/formulas/<domain>.json` following the schema in
   `knowledge/formulas.py` (name, equation, domain, variables+units,
   assumptions, validity, related, mistakes, applications, difficulty,
   keywords, source).
4. Add tests under `tests/physics/test_<domain>.py` with analytic reference
   values (tolerance-based asserts, no randomness unless seeded).
5. Add at least one worked example under `examples/`.

## Adding a solver / tool

- Solvers live in `solvers/` and `mathematics/`; they must be deterministic,
  typed, and LLM-independent.
- Expose them through `tools/registry.py` as a `Tool` with a JSON-schema
  `parameters` dict and a docstringed function.
- Add unit tests exercising success *and* failure paths.

## Knowledge & constants

- Constants go in `data/constants/*.json` (SI value, unit, description,
  source, precision). Never hard-code physical constants in solver code —
  import them from `knowledge/constants.py`.
- Knowledge items need topic/subtopic/equation/explanation/assumptions/
  source/difficulty/keywords/related so the future RAG index can ingest
  them unchanged.

## Code quality bar

- Type hints on all public functions; docstrings with units and assumptions.
- `pytest` green; new code covered by tests with analytic cross-checks.
- Dimensional checks on every new physics function returning a quantity.
- No network calls in the computation layer; LLM code stays in `llm/`.
