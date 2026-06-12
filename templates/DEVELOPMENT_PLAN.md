# Development Plan — [Project Name]

**Version:** 1.0
**Date:** [YYYY-MM-DD]
**Status:** draft

---

## Overview

[2-3 sentences: what is being built and what V1 delivers]

---

## Scope

**In V1:**
- [item]
- [item]

**Out of V1 (explicit):**
- [item]
- [item]

---

## Components and phases

One phase per component, dependency-ordered. The final phase is integration.

### Phase 1 — [Component name]

**Goal:** [what this component delivers — one sentence]
**Depends on:** nothing / [components, faked until integration]
**Fakes required:** [FakeX in tests/fakes/ — or none]
**Gate:** `[named command, e.g. pytest tests/contract/test_<component>.py]` exits 0

See TASKS.md §Phase 1 for the task breakdown.

### Phase 2 — [Component name]

**Goal:** [what this component delivers]
**Depends on:** Phase 1
**Fakes required:** [or none]
**Gate:** `[named command]` exits 0

See TASKS.md §Phase 2 for the task breakdown.

### Phase N — Integration

**Goal:** replace fakes with real components; system works end-to-end
**Gate:** `[named end-to-end command]` exits 0

Fake retirement is one explicit task per dependency; integration tests are
specified here at planning time, never improvised during the endgame.

---

## Dependencies and Integration Points

| Component | Depends on | Interface |
|-----------|-----------|-----------|
| [component] | [what] | [brief description] |

---

## Risks and Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk description] | high/med/low | high/med/low | [mitigation plan] |

---

## Open Questions

Questions that must be resolved before implementation can start:

- [ ] [question — assign to Architect, Planner, or User]

---

## Decision Log

Implementation-phase decisions are in `AGENT_LOG.md`.
Blueprint deviations are in `DEVIATIONS.md`.
