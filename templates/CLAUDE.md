# [Project Name] — Claude Instructions

This project uses the **agentic-dev-workflow**. Three specialized agents handle design, planning, and implementation.

---

## Key Files

| File | Purpose | Written by |
|------|---------|-----------|
| `*_BLUEPRINT.md` | Architecture and design specifications | Architect |
| `DEVELOPMENT_PLAN.md` | Phases, milestones, risks | Planner |
| `TASKS.md` | Granular task checklist | Planner |
| `AGENT_LOG.md` | Inter-agent decision log | Developer + Planner |
| `DEVIATIONS.md` | Implementation deviations from blueprint | Developer |
| `CLARIFICATIONS.md` | Resolved blueprint ambiguities | Planner / Developer |
| `DEVLOG.md` | Developer session log | Developer |

---

## Workflow

```
/architect   → design or update blueprints (talk with user)
/planner     → create or update DEVELOPMENT_PLAN.md + TASKS.md
/developer   → implement tasks from TASKS.md (autonomous)
```

Planner and Architect are also spawned automatically as subagents by Developer — you do not need to invoke them manually for blocking questions during implementation.

---

## Rules for All Agents

1. Read before editing — never assume the current state of a file
2. Do not implement anything not in `TASKS.md` without adding it first
3. Do not modify blueprints during implementation — route through Planner → Architect
4. Log all deviations in `DEVIATIONS.md` immediately
5. Mark `TASKS.md` tasks complete as they are done — not at session end
6. Write to `AGENT_LOG.md` before every subagent call

---

## Project-Specific Notes

[Add any project-specific constraints, conventions, or context here.]
