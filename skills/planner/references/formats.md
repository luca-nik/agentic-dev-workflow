# Planner — Output Formats

You produce three artifacts in `agentic/plan/`:

1. `TASKS.md` — the index and checklist (one line per task)
2. `tasks/TASK-NNN.md` — one **work order** per task (the full, self-contained definition)
3. `DEVELOPMENT_PLAN.md` — phases, components, risks

---

## TASKS.md (index)

```markdown
# Tasks — [Project Name]

**Last updated:** [date]
**Active phase:** Phase [N] — [component]

---

## Phase 1 — [Component name]

- [ ] TASK-001: [imperative title] → `tasks/TASK-001.md`
- [ ] TASK-002: [imperative title] → `tasks/TASK-002.md`
- [ ] TASK-003: GATE — [component] contract tests green → `tasks/TASK-003.md`

## Phase 2 — [Component name]

- [ ] TASK-004: [imperative title] → `tasks/TASK-004.md`
...

## Phase N — Integration

- [ ] TASK-0NN: replace Fake[X] with [X], delete Fake[X], integration tests green → `tasks/TASK-0NN.md`
...

---

## Backlog (unscheduled)

- [ ] TASK-0NN: [title — lower priority, not blocking V1]

## Completed

<!-- moved here as tasks are done, with completion date -->
```

Conventions:

- Task IDs are **globally sequential** (TASK-001, TASK-002, …) across all phases and
  the backlog — never per-phase ID ranges. IDs are never reused.
- Mark `[x]` on completion immediately — not at session end
- Mark `[~]` for partial: `[~] TASK-NNN: title — partial: [what remains]`
- Every entry links its work order
- The **last task of every component phase is the gate task** (see Component phasing)

---

## Work order — `agentic/plan/tasks/TASK-NNN.md`

```markdown
# TASK-NNN — [imperative title]

**Component:** [component name]
**Goal:** [one sentence]
**Executor tier:** strong | standard | economy — [one-line justification]
**Execution mode:** executor | operator
**Human review:** required | none

## Contract

[3–4 line summary of the interface/behavior this task must honor]

Source of truth: [BLUEPRINT_FILE.md §sections]. If this summary and the blueprint
disagree, the blueprint wins — report the mismatch in your result.

## Read first

- [file, or blueprint §section — the complete manifest; nothing else is assumed read]

## Workspace preconditions

- [what earlier tasks already created that this task relies on, e.g.
  "TASK-012 wrote `src/models.py` with class Invoice — it exists"]

## Environment

[how to run the acceptance commands: setup steps (e.g. `uv sync`), working
directory, required env vars]

## Modify

- [files to create or change — nothing outside this list]

## Acceptance criteria

- [ ] `[command]` exits 0
- [ ] [behavioral criterion, concrete: input X → output Y]

## Do not

- [explicit boundaries: interfaces not to touch, no new dependencies, …]

## If unspecified

- [trigger: "if X is ambiguous"] → return NEEDS_DECISION with your analysis;
  do not improvise. Escalate BEFORE modifying files when the ambiguity is
  detectable up front.

## Docs to update

- [optional; mandatory when the project has a doc-contract that treats
  staleness as a defect]
```

Field rules:

- **Self-containment test:** a fresh executor that reads only this file plus the
  items in *Read first* must be able to complete the task. If it can't, the work
  order is incomplete — fix the work order, not the executor.
- **Contract:** pointer + short summary; the blueprint is always the source of truth.
- **Acceptance criteria:** machine-checkable (commands) wherever possible; behavioral
  criteria must be concrete enough to become a test.
- **Executor tier:** if the acceptance criteria fully pin the behavior, tier down
  (economy); if correctness requires judgment the criteria can't capture
  (statistical logic, prompt engineering, numerically subtle code), tier up (strong).
  Default: standard.
- **Execution mode:** `executor` (default — fresh spawned subagent). `operator` for
  tasks needing live API keys, paid third-party services, or long external runs
  (30+ min): the orchestrator surfaces these to the top-level session/user instead
  of spawning.
- **Human review:** `required` pauses the orchestrator after the task until the user
  has reviewed the produced artifact. Use for trust-anchor artifacts that downstream
  tasks consume.
- **A work order specifies contract and boundaries, never the implementation.**
  Prose-code in a work order is a planning defect.
- **Bundling:** small, same-component, same-files tasks may share one work order
  (one TASK ID, multiple acceptance criteria) instead of spawning one executor each.

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

## Components and phases

One phase per component, dependency-ordered. Final phase is integration.

### Phase 1 — [Component name]
**Goal:** [what this component delivers]
**Depends on:** nothing / [components, faked until integration]
**Fakes required:** [FakeX in tests/fakes/ — or none]
**Gate:** `[named command, e.g. pytest tests/contract/test_<component>.py]` exits 0

### Phase N — Integration
**Goal:** replace fakes with real components; system works end-to-end
**Gate:** `[named end-to-end command]` exits 0

## Risks and Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

## Open Questions

- [ ] [question needing resolution before implementation can start]
```

---

## Component phasing rules

1. **One phase per component**, ordered so no component depends on a later one.
2. **Fakes for unbuilt dependencies:** each fake implements the blueprint interface
   *exactly* (same signatures, same schemas), lives in `tests/fakes/`, and is
   written as an explicit task — never improvised.
3. **The gate is a named command**, not a sentence: the last task of the phase is
   "GATE — contract tests green", with the command in its acceptance criteria.
4. **Integration is planned at planning time:** integration tests are tasks with
   acceptance commands, and retiring each fake is an explicit task
   ("replace FakeX with X; delete FakeX; integration tests green").
   Nothing about the endgame is improvised during implementation.
