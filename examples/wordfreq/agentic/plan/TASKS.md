# Tasks — wordfreq

**Last updated:** 2026-06-14
**Active phase:** Phase 2 — counter

Task IDs are globally sequential across all phases and the backlog; IDs are never
reused. Each entry links its work order in `tasks/`. The last task of every component
phase is the gate task.

---

## Phase 1 — tokenizer

- [x] TASK-001: implement `tokenize(text)` in `src/wordfreq/tokenizer.py` → `tasks/TASK-001.md` *(completed 2026-06-14)*
- [x] TASK-002: GATE — tokenizer contract tests green → `tasks/TASK-002.md` *(completed 2026-06-14)*

## Phase 2 — counter

- [ ] TASK-003: add `FakeTokenizer` in `tests/fakes/fake_tokenizer.py` → `tasks/TASK-003.md`
- [ ] TASK-004: implement `count_frequencies` + `top_n` in `src/wordfreq/counter.py` → `tasks/TASK-004.md`
- [ ] TASK-005: GATE — counter contract tests green → `tasks/TASK-005.md`

## Phase 3 — Integration

- [ ] TASK-006: replace `FakeTokenizer` with real tokenizer; delete fake; integration tests green → `tasks/TASK-006.md`

---

## Backlog (unscheduled)

- [ ] TASK-007: CLI wrapper (`wordfreq FILE --top 10`)

## Completed

- [x] TASK-001: implement `tokenize(text)` *(2026-06-14)*
- [x] TASK-002: GATE — tokenizer contract tests green *(2026-06-14)*
