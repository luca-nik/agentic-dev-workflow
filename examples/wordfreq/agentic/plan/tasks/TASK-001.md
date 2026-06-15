# TASK-001 — Implement `tokenize(text)` in src/wordfreq/tokenizer.py

**Component:** tokenizer
**Goal:** a leaf function that splits and normalizes a string into an ordered token list.
**Executor tier:** economy — behavior fully pinned by the acceptance examples.
**Execution mode:** executor
**Human review:** none

## Contract

`tokenize(text: str) -> list[str]`. Lowercases via `str.casefold()`; every
non-alphanumeric character is a separator; tokens preserve first-occurrence order;
empty/whitespace input → `[]`; non-string input → `TypeError`.

Source of truth: `agentic/blueprints/TOKENIZER_BLUEPRINT.md` §2 (acceptance table) and
§4 (architectural decisions). If this summary and the blueprint disagree, the blueprint
wins — report the mismatch.

## Read first

- `agentic/blueprints/TOKENIZER_BLUEPRINT.md`

## Workspace preconditions

- None — this is the leaf task. `src/wordfreq/` may not exist yet; create it with an
  `__init__.py`.

## Environment

From `examples/wordfreq/`: `python -m pytest -q` runs the suite. No third-party
dependencies.

## Modify

- `src/wordfreq/__init__.py` (create, empty)
- `src/wordfreq/tokenizer.py` (create)
- `tests/unit/test_tokenizer.py` (create — your white-box unit tests)

## Acceptance criteria

- [ ] `python -m pytest tests/unit/test_tokenizer.py tests/contract/test_tokenizer.py -q` exits 0
- [ ] `tokenize("Hello, world!") == ["hello", "world"]`
- [ ] `tokenize("") == []`
- [ ] `tokenize("Don't") == ["don", "t"]`
- [ ] `tokenize(None)` raises `TypeError`

## Do not

- Do not add token offsets, NFKD normalization, or a streaming interface — §6 out of scope.
- Do not import any other `wordfreq` module.
- Do not add third-party dependencies.

## If unspecified

- If a behavior is not pinned by the acceptance table (e.g., a locale-specific
  casefold edge case), return `NEEDS_DECISION` with the example — do not improvise.

## Docs to update

- None.
