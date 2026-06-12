# Agent Log — [Project Name]

Inter-agent conversation log. Each exchange is recorded as two entries: a **question entry** written by the asking agent before spawning the subagent, and a **response entry** appended by the responding agent.

This file is append-only. Do not edit past entries. Decision IDs (DEC-NNN) are assigned only in response entries, by the responding agent (Planner or Architect), incrementing from the last DEC in the file. Log-writing subagent calls must be sequential — never two concurrently.

---

<!--
Question entry (written by the asking agent BEFORE spawning the subagent):

## [YYYY-MM-DDTHH:MM:SS] — [From] → [To] (question)

**Context:** [what triggered this exchange]
**Question:** [the specific blocking question]
**What I established:** [the asker's analysis before escalating]

Response entry (appended by the responding agent):

## [YYYY-MM-DDTHH:MM:SS] — [Responder] (response to [question entry timestamp])

**Reasoning:** [analysis of blueprints/code that led to the decision]
**Decision:** [the concrete answer]
**Escalated to Architect:** yes / no
**Escalated to User:** yes / no
**Decision ID:** DEC-NNN

In a two-hop chain (Developer → Planner → Architect) the Architect appends its own
response entry with its own DEC, and the Planner's response entry references it:
two entries, two IDs, appended in completion order.
-->
