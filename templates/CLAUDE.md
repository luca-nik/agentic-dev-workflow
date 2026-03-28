# [Project Name] — Claude Instructions

This project uses the **agentic-dev-workflow**. Three specialized agents handle design, planning, and implementation.

---

## Folder Structure

```
agentic/
  blueprints/     ← *_BLUEPRINT.md files (Architect)
  plan/           ← DEVELOPMENT_PLAN.md, TASKS.md (Planner)
  logs/           ← AGENT_LOG.md, DEVLOG.md, DEVIATIONS.md, CLARIFICATIONS.md (all agents)
```

---

## Key Files

| File | Purpose | Written by |
|------|---------|-----------|
| `agentic/blueprints/*_BLUEPRINT.md` | Architecture and design specifications | Architect |
| `agentic/plan/DEVELOPMENT_PLAN.md` | Phases, milestones, risks | Planner |
| `agentic/plan/TASKS.md` | Granular task checklist | Planner |
| `agentic/logs/AGENT_LOG.md` | Inter-agent decision log | Developer + Planner |
| `agentic/logs/DEVIATIONS.md` | Implementation deviations from blueprint | Developer |
| `agentic/logs/CLARIFICATIONS.md` | Resolved blueprint ambiguities | Planner / Developer |
| `agentic/logs/DEVLOG.md` | Developer session log | Developer |

---

## Workflow

```
/architect   → design or update blueprints (talk with user)
/planner     → create or update agentic/plan/ files
/developer   → implement tasks from agentic/plan/TASKS.md (autonomous)
```

Planner and Architect are also spawned automatically as subagents by Developer — you do not need to invoke them manually for blocking questions during implementation.

---

## Rules for All Agents

1. Read before editing — never assume the current state of a file
2. Do not implement anything not in `agentic/plan/TASKS.md` without adding it first
3. Do not modify `agentic/blueprints/` during implementation — route through Planner → Architect
4. Log all deviations in `agentic/logs/DEVIATIONS.md` immediately
5. Mark tasks complete in `agentic/plan/TASKS.md` as they are done — not at session end
6. Write to `agentic/logs/AGENT_LOG.md` before every subagent call

---

## Project-Specific Notes

[Add any project-specific constraints, conventions, or context here.]
