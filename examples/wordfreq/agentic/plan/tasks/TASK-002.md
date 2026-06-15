# TASK-002 — GATE: tokenizer contract tests green

**Component:** tokenizer
**Goal:** an independent black-box verification that the implementation honors the blueprint.
**Executor tier:** strong — this task spawns the Verifier (gate), not an executor.
**Execution mode:** executor
**Human review:** none

## Contract

The Verifier derives contract tests from `TOKENIZER_BLUEPRINT.md` §2 and runs them
against `src/wordfreq/tokenizer.py`. This is the Phase 1 gate.

Source of truth: `agentic/blueprints/TOKENIZER_BLUEPRINT.md`.

## Read first

- `agentic/blueprints/TOKENIZER_BLUEPRINT.md`
- `agentic/plan/tasks/TASK-001.md` (acceptance criteria — read only AFTER deriving tests)

## Environment

From `examples/wordfreq/`: `python -m pytest -q`.

## Modify

- `tests/contract/test_tokenizer.py` (created by the Verifier)

## Acceptance criteria

- [ ] `python -m pytest tests/contract/test_tokenizer.py -q` exits 0
- [ ] Verifier report `VERDICT: pass`

## Do not

- The Verifier must not read `src/wordfreq/tokenizer.py` bodies, `tests/unit/`, or
  `DEVLOG.md`. It verifies the contract, not the process.

## If unspecified

- If the blueprint is too vague to derive a test from, the Verifier returns
  `VERDICT: blocked`; route to Planner → Architect.
