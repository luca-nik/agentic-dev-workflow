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

## agentic/logs/AGENT_LOG.md — Question entry (written by Developer before spawning Planner)

```markdown
## [YYYY-MM-DDTHH:MM:SS] — Developer → Planner (question)

**Context:** Implementing [TASK-NNN: description]
**Question:** [blocking question]
**What I established:** [analysis before escalating]
```

No Decision ID and no fields left "to be filled" — the log is append-only and past entries are never edited. The Planner appends its own response entry (referencing this entry's timestamp) and assigns the Decision ID there.

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
