# Developer — Log Formats

## agentic/logs/DEVLOG.md

Append at session start (before any code changes):
```markdown
## [YYYY-MM-DD] — Session [N]

### Start
Tasks targeted: TASK-NNN, TASK-NNN, ...
Conventions brief (seeded from previous session, or empty):
[the brief]
```

Append at session end:
```markdown
### End
Implemented: [TASK-NNN list]
Skipped: [list with reason]
Blockers remaining: [list]
Subagent calls: [N executors, N Planner, N Architect]
Conventions brief (current — the next session seeds from this):
[the brief — relevant DEC decisions, doc-contract obligations, naming/test
conventions observed; hard cap half a page]
```

---

## Commits

One commit per completed task, made by the orchestrator **after** the mechanical
acceptance check passes, message: `TASK-NNN: [title]`. Never batch tasks into one
commit. If the project is not a git repository, skip and note it in DEVLOG.

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

Deviations are information, not failures. Log them without judgment. The DEV entry is written by the executor that implemented the deviation, as part of its task.

---

## TASKS.md conventions

- Mark `[x]` on completion immediately — not at session end
- Mark `[~]` for partial: `[~] TASK-NNN: description — partial: [what remains]`
