# Developer — Log Formats

## agentic/logs/DEVLOG.md

Append at session start (before any code changes):
```markdown
## [YYYY-MM-DD] — Session [N]

### Start
Tasks targeted: TASK-NNN, TASK-NNN, ...
```

Append at session end:
```markdown
### End
Implemented: [TASK-NNN list]
Skipped: [list with reason]
Blockers remaining: [list]
Subagent calls: [N Planner, N Architect]
```

---

## agentic/logs/AGENT_LOG.md — Pre-call entry (written by Developer before spawning Planner)

```markdown
## [YYYY-MM-DDTHH:MM:SS] — Developer → Planner

**Context:** Implementing [TASK-NNN: description]
**Question:** [blocking question]
**What I established:** [analysis before escalating]
**Decision:** [to be filled by Planner]
**Escalated to Architect:** [to be filled by Planner]
**Escalated to User:** [to be filled by Planner]
**Decision ID:** DEC-[NNN]
```

The Planner fills in the remaining fields when it responds.

---

## agentic/logs/DEVIATIONS.md entry

```markdown
## DEV-[NNN] — [YYYY-MM-DD]

**Task:** TASK-NNN
**Blueprint says:** [exact specification — quote it]
**Implemented:** [what was actually done]
**Reason:** [why the blueprint couldn't be followed]
**Decision ID:** DEC-NNN (if Planner was involved) / none
```

Deviations are information, not failures. Log them without judgment.

---

## TASKS.md conventions

- Mark `[x]` on completion immediately — not at session end
- Mark `[~]` for partial: `[~] TASK-NNN: description — partial: [what remains]`
