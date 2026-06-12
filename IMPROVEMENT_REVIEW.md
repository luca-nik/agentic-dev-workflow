# Independent Review of IMPROVEMENT_REPORT.md

**Date:** 2026-06-12
**Reviewer:** independent QC agent (per IMPROVEMENT_REPORT.md §6)
**Verdict:** **Approve with required changes.** The diagnosis is accurate — every
functional defect (P1–P4) was verified directly in the source, one of them empirically in
a real project session. The redesign decisions (D1–D12) are sound. Before implementation
begins, the required changes in §3 must be folded into the report/phases; the
recommendations in §4 should be considered; §5 records requirements from the first
consumer project that the new workflow must support.

---

## 1. Verification of the diagnosis

| Problem | Verified | Evidence |
|---|---|---|
| P1 no subagent→user channel | ✅ | README mermaid `AS2 -- needs user input? --> U`; `architect/SKILL.md` §"When Invoked as Subagent" instructs "ask the user". Agent-tool subagents are non-interactive; the path cannot exist. |
| P2 spawned agents never load SKILL.md | ✅ | `developer/SKILL.md` §"Spawning the Planner" and `planner/SKILL.md` §"Spawning the Architect": both inline ~10-line prompts, neither references the skill file. |
| P3 AGENT_LOG contradictions | ✅ | `templates/AGENT_LOG.md` "append-only / do not edit past entries" vs `developer/references/formats.md` "The Planner fills in the remaining fields"; `What I established` vs `Reasoning`; DEC assigned in both the Developer pre-call format and `planner/SKILL.md` ("increment from the last entry"). |
| P4 CLARIFICATIONS.md orphaned | ✅ + empirical | No write instruction in either planner or developer SKILL.md while `templates/CLAUDE.md` names them writers. **Field confirmation:** in a real session (2026-06-11, digital-twin-pipeline project) the file was populated only because the session model chose to, outside any skill instruction. A literal-minded model leaves it empty — exactly as P4 predicts. |

P5–P8 are correctly identified; P6 (self-grading) is the deepest and D9 is the right
class of fix. No misdiagnoses found.

---

## 2. Answers to the §6 review questions

**Q1 — Does D1 close P1?** Yes, *provided* the rewrite list is complete. The report
mentions spawn templates and `architect/SKILL.md` §"When Invoked as Subagent". Three more
places assert or imply the impossible path and must be rewritten in the same pass:

1. README mermaid diagram (both `AS -- needs user input --> U` arrows).
2. README §"The Three Agents": "**Always asks the user** when context is insufficient —
   even when spawned as a subagent."
3. `developer/SKILL.md` §"AskUserQuestion — last resort": "Only after Planner returns
   'requires user input'" — reword to the sentinel contract (`NEEDS_USER_INPUT`
   propagated up; the top-level agent asks).

After those, no path remains where a subagent reaches the user directly.

**Q2 — Is D3 conflict-free under nesting?** Only under **sequential** subagent calls.
Two responders running concurrently would both read "last DEC" and collide. Either (a)
state the constraint explicitly in all skills — *never run two log-writing subagents
concurrently* — or (b) namespace IDs (`DEC-<sessionid>-NNN`). Option (a) is fine for the
current sequential workflow; pick one and write it down. Also specify the two-hop case
explicitly: in Developer→Planner→Architect, the Architect's response entry carries its
own DEC, and the Planner's response entry references it — two entries, two IDs, appended
in completion order.

**Q3 — Is the D5 work-order format sufficient for a weaker model?** Close, but missing
five fields. Add to the required format:

1. **Environment** — how to run the acceptance commands (setup steps, e.g. `uv sync`,
   working directory, env vars). A weak executor must not have to discover this.
2. **Workspace preconditions** — what earlier tasks already created ("TASK-012 wrote
   `data/calibration/noise_floor.json`; it exists").
3. **Partial-work protocol** — see §3.1 below.
4. **Executor tier** — see §3.2 below.
5. **Execution mode** — `executor | orchestrator | operator`; see §5.2 below.

Optionally a **Docs to update** field (consumer projects often have a doc-contract, e.g.
"new files must be added to the project's pipeline reference"; staleness there is a
defect).

**Q4 — Does D9 break the self-grading loop?** It breaks the *executor* self-grading
loop genuinely. Bias can still leak through the Planner's acceptance criteria into both
executor and Verifier. The report's mitigation (blueprint-first derivation, criteria as a
coverage checklist afterwards) is correct — make the ordering a **hard rule** in the
Verifier skill, not prose. Two additions: (a) the Verifier's "do not read" list
(implementation internals, executor tests, DEVLOG) must appear as an explicit Do-not
block in its skill file; (b) be honest in the README that two LLM actors share training
priors — the Verifier reduces correlated misreading, it does not eliminate it. The
mechanical checks (D8) and the user's plan-approval gate are the only fully independent
verdicts; say so.

**Q5 — Is the D10 integration phase concrete enough?** No — this is the weakest section,
as the report itself suspects. Concretize with four rules:

1. Fakes implement the blueprint interface **exactly** (same signatures, same schemas),
   live in a dedicated `tests/fakes/`, and are written as explicit tasks.
2. Integration tests are specified by the **Planner at planning time** (as tasks with
   acceptance commands), never improvised during the endgame.
3. Fake retirement is an explicit task per dependency ("replace FakeX with X; delete
   FakeX; integration tests green").
4. The component gate is a named command ("`pytest tests/contract/test_<component>.py`
   exits 0"), not a sentence.

**Q6 — Remaining contradictions not covered by Phases 0–3?** Four found — all must be
added to Phase 0's scope (the report currently fixes skills but does not list template
and README sync):

1. `templates/CLAUDE.md` key-files table: CLARIFICATIONS writer "Planner / Developer"
   contradicts D4 (Planner only).
2. `templates/CLAUDE.md` rule 6 ("Write to AGENT_LOG.md before every subagent call") is
   compatible with D3 only if the pre-call entry format changes; the rule's wording
   should reference the new question-entry format (no DEC, no to-be-filled fields).
3. `templates/AGENT_LOG.md` comment block shows a single merged entry format (both
   `Reasoning` and the response fields in one entry) — must become two entry types
   (question entry / response entry).
4. README decision-authority matrix duplicated in three SKILL.md files: the risk table
   already proposes declaring README non-normative — do it in Phase 0 (one line: "the
   SKILL.md files are normative; this README is descriptive").

---

## 3. Required changes (blocking — fold into the report before implementing)

### 3.1 Partial-work protocol on escalation (gap in D1/D7)

D1 re-spawns a blocked executor fresh with the answer included — but a mid-task executor
may already have edited files. Required: (a) work orders instruct executors to escalate
**before** modifying files when the ambiguity is detectable up front (the "If
unspecified" triggers exist for exactly this); (b) when a mid-work block is unavoidable,
the `NEEDS_DECISION` return must include a workspace-state summary (files touched, state
of each), and the orchestrator must include it in the re-spawn prompt.

### 3.2 Per-task model tiering (D11 is per-role; must be per-task)

Sending *all* executors to cheap models is wrong whenever the judgment lives inside the
task (statistical logic, prompt engineering, numerically subtle code). The Planner sets
an **executor tier** field per work order; D11's default (cheap) applies only where the
work order says so. Rule of thumb for the Planner: if the acceptance criteria fully pin
the behavior, tier down; if correctness requires judgment the criteria can't capture,
tier up.

### 3.3 Cost control for the orchestrator model (gap in D7)

Fresh executor + manifest reading per task multiplies tokens; for trivial tasks the
overhead exceeds the work. Add either: a Planner bundling rule (small, same-component,
same-files tasks may share one work order) or an orchestrator size threshold (single
file, no interface surface, one acceptance command ⇒ orchestrator executes directly).
Pick one mechanism; leaving it unspecified guarantees inconsistent behavior.

### 3.4 Phase 0 scope completion

Add the four §2-Q6 items plus the three §2-Q1 rewrite locations to Phase 0 explicitly.
Phase 0's definition of done: no document in the repo asserts a behavior the mechanics
make impossible, and no two documents disagree on a format.

### 3.5 Resolve the orchestrator source-reading rule (ambiguity in D7)

"The orchestrator never reads source code" collides with "the orchestrator patches
downstream work orders on impacts" — patching sometimes requires confirming an
interface. Pick one: (a) keep the rule absolute and route all work-order patches through
a Planner spawn, or (b) allow a narrow exception ("may read interface/signature lines
strictly to patch a work order; never implementation bodies"). Either is defensible;
ambiguity is not.

### 3.6 Verifier round cap becomes skill text

The risk table caps Verifier rounds at 2, escalating the third failure to the Planner as
a design defect. Move this from the risk table into the Verifier and orchestrator skill
files as a hard rule — risk tables don't execute.

---

## 4. Recommendations (non-blocking)

1. **Git discipline.** Commit per task (orchestrator commits after the D8 check passes,
   task ID in the message). Cheap executors with no VCS checkpoints is the riskiest
   combination in the whole design; per-task commits make every executor mistake
   cheaply revertible. Strongly recommended even though not strictly part of the agent
   contracts.
2. **Conventions brief contents (D7).** Specify what goes in it: accumulated DEC
   decisions relevant to the component, project doc-contract obligations, naming/test
   conventions observed so far. Cap its size (~½ page) so it doesn't become a second
   context rot vector.
3. **Acceptance for the improvement work itself.** Run the upgraded workflow end-to-end
   on a small real example and commit the resulting `agentic/` tree as `examples/` —
   this simultaneously validates Phases 0–3 and closes the P9 examples gap.
4. **`ln -sfn` and CI lint** (P9) are correctly parked in Phase 4; no objection.

---

## 5. Requirements from the first consumer project (digital-twin-pipeline)

The first real project to run under the upgraded workflow is a validation/calibration
pipeline whose plan (27 tasks, 6 phases) will be regenerated as work orders by the new
Planner. It stresses the design in ways the report should anticipate:

1. **Human-review checkpoints inside phases, not only at gates.** One task produces a
   human-owned trust-anchor file (a reference interpreter) that **must be human-reviewed
   before downstream tasks may consume it**, and is agent-protected afterwards. The
   work-order format needs a `human_review_required: true` flag, and the orchestrator
   must pause on it (this is a *blocking* user interaction by design — distinct from
   NEEDS_USER_INPUT escalation, which is exceptional).
2. **Operator tasks.** Several tasks need live API keys, paid third-party services, or
   30+ minute external pipeline runs — unsuitable for spawned executors (timeouts,
   interactivity). Hence the `execution: operator` mode in §2-Q3: the orchestrator
   surfaces these to the user/top-level session instead of spawning.
3. **Doc-contract obligations.** The project's pipeline reference document treats
   staleness as a defect; every work order touching pipeline files must carry the
   doc-update obligation (the optional "Docs to update" field in §2-Q3 becomes
   load-bearing here).
4. **Judgment-dense tasks.** Statistical gate logic and LLM-phase prompt engineering
   must not be tiered down (§3.2): the consumer project is the concrete argument for
   per-task tiering.

---

## 6. Sequencing opinion

Phase ordering in the report is correct (0 independent and first; 1 prerequisite of 2–3).
For the consumer project above: Phases 0–2 are sufficient to begin implementation under
the new workflow (work orders + orchestrator + mechanical checks); Phase 3 (Verifier)
can land during the consumer project's first component phase and apply from its first
gate onward. Phase 4 should not delay anything.
