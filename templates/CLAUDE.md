# [Project Name] — Claude Instructions

This project uses the **agentic-dev-workflow**. Four specialized agents handle design, planning, implementation, and verification.

---

## Folder Structure

```
agentic/
  blueprints/     ← *_BLUEPRINT.md files (Architect)
  plan/           ← DEVELOPMENT_PLAN.md, TASKS.md, tasks/TASK-NNN.md (Planner)
  logs/           ← AGENT_LOG.md, DEVLOG.md, DEVIATIONS.md, CLARIFICATIONS.md (all agents)
```

---

## Key Files

| File | Purpose | Written by |
|------|---------|-----------|
| `agentic/blueprints/*_BLUEPRINT.md` | Architecture and design specifications | Architect |
| `agentic/plan/DEVELOPMENT_PLAN.md` | Phases, milestones, risks | Planner |
| `agentic/plan/TASKS.md` | Task index and checklist | Planner |
| `agentic/plan/tasks/TASK-NNN.md` | Self-contained work order per task | Planner |
| `agentic/logs/AGENT_LOG.md` | Inter-agent decision log | Developer + Planner |
| `agentic/logs/DEVIATIONS.md` | Implementation deviations from blueprint | Developer |
| `agentic/logs/CLARIFICATIONS.md` | Resolved blueprint ambiguities | Planner |
| `agentic/logs/DEVLOG.md` | Developer session log | Developer |

---

## Workflow

```
/architect   → design or update blueprints (talk with user)
/planner     → create or update agentic/plan/ files (index + work orders)
/developer   → orchestrate implementation of agentic/plan/TASKS.md (autonomous)
/verifier    → independent black-box contract check of a component
```

Planner, Architect, and Verifier are also spawned automatically as subagents by Developer — you do not need to invoke them manually during implementation. Contract tests written by the Verifier live in `tests/contract/`.

---

## Rules for All Agents

1. Read before editing — never assume the current state of a file
2. Do not implement anything not in `agentic/plan/TASKS.md` without adding it first
3. Do not modify `agentic/blueprints/` during implementation — route through Planner → Architect
4. Log all deviations in `agentic/logs/DEVIATIONS.md` immediately
5. Mark tasks complete in `agentic/plan/TASKS.md` as they are done — not at session end
6. Append a question entry to `agentic/logs/AGENT_LOG.md` before every subagent call — the log is append-only; the responder appends its own response entry and assigns the Decision ID there
7. Subagents never address the user directly — a blocked subagent returns `NEEDS_USER_INPUT` to its spawner, and only the top-level agent asks the user
8. One commit per completed task (`TASK-NNN: title`), made after the task's acceptance commands pass — when the project is a git repository

---

## Project-Specific Notes

[Add any project-specific constraints, conventions, or context here.]
