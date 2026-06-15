# Development Plan — wordfreq

**Version:** 1.0
**Date:** 2026-06-14
**Status:** active

## Overview

A tiny word-frequency library: a tokenizer and a counter. V1 delivers a working
end-to-end pipeline over in-memory strings.

## Scope

**In V1:**

- `tokenize(text) -> list[str]`
- `count_frequencies(tokens) -> dict[str, int]`
- `top_n(tokens, n) -> list[tuple[str, int]]`

**Out of V1 (explicit):**

- unicode NFKD normalization
- streaming / generator tokenization
- token offsets

## Components and phases

### Phase 1 — tokenizer

**Goal:** a leaf component that splits and normalizes a string into tokens.
**Depends on:** nothing.
**Fakes required:** none.
**Gate:** `python -m pytest tests/contract/test_tokenizer.py -q` exits 0.

### Phase 2 — counter

**Goal:** frequency counting and top-N over a token list.
**Depends on:** tokenizer contract (faked until integration).
**Fakes required:** `FakeTokenizer` in `tests/fakes/` — written as TASK-003.
**Gate:** `python -m pytest tests/contract/test_counter.py -q` exits 0.

### Phase 3 — Integration

**Goal:** retire the fake; system works end-to-end.
**Gate:** `python -m pytest tests/integration/ -q` exits 0.

Fake retirement is one explicit task (`tests/fakes/fake_tokenizer.py` deleted once the
integration tests pass against the real tokenizer). Integration tests are specified now,
not improvised during the endgame.

## Risks and Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Case-folding ambiguity (locale-specific) | low | med | casefold() decided in blueprint AD-1 |
| Tie-breaking nondeterminism in top_n | med | low | first-occurrence order specified |

## Open Questions

- [ ] none remaining — Phase 1 unblocked.
