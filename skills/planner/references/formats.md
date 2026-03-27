# Planner — Output Formats

## TASKS.md

```markdown
# Tasks — [Project Name]

**Last updated:** [date]
**Active phase:** Phase [N]

---

## Phase 1 — [Name]

- [ ] TASK-001: [description] `[primary file(s) affected]`
- [ ] TASK-002: [description] `[primary file(s) affected]`

## Phase 2 — [Name]

- [ ] TASK-010: [description] `[primary file(s) affected]`

---

## Backlog (unscheduled)

- [ ] TASK-100: [description]

## Completed

- [x] TASK-000: [description] *(completed [date])*
```

Tasks must be:
- Implementable in a single Developer session (small enough to complete and verify)
- Ordered by dependency — no task depends on a later task
- Specific enough that Developer implements without designing

---

## DEVELOPMENT_PLAN.md

```markdown
# Development Plan — [Project Name]

**Version:** 1.0
**Date:** [date]
**Status:** draft / active / complete

## Overview

[2-3 sentences: what is being built and what V1 delivers]

## Scope

**In V1:** [bullet list]
**Out of V1:** [bullet list]

## Phases

### Phase 1 — [Name]
**Goal:** [what this phase delivers]
**Deliverable:** [concrete artifact or capability]
**Depends on:** nothing / Phase N

### Phase 2 — [Name]
...

## Risks and Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

## Open Questions

- [ ] [question needing resolution before implementation can start]
```
