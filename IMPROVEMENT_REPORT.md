# Pipeline Improvement Report

**Date:** 2026-06-12
**Status:** independently reviewed (see `IMPROVEMENT_REVIEW.md` — verdict: approve with
required changes); all blocking changes from the review are folded in below.
**Phase 0 implemented 2026-06-12** (skills, templates, README synchronized to D1–D4).
**Phase 1 implemented 2026-06-12** (work orders, component phasing, testable contracts —
D5, D6, D10, D13 fields, D14).
**Phase 2 implemented 2026-06-12** (Developer orchestrator, fresh executors, mechanical
checks, per-task commits — D7, D8, D11, D13 modes).
**Phase 3 implemented 2026-06-12** (Verifier skill + gate protocol — D9, D12).
Next: Phase 4 (portfolio polish: examples/ from a real session, CI lint).
**Audience:** this is a working document. It records the problems found in the current
workflow and the redesign decisions made to fix them. It is written to be reviewed by an
independent agent for quality control before implementation begins.

---

## 1. What this repository is

A three-agent workflow for Claude Code: **Architect** (designs, writes blueprints),
**Planner** (turns blueprints into `DEVELOPMENT_PLAN.md` + `TASKS.md`), **Developer**
(implements tasks autonomously). Agents escalate through a decision-authority chain
(Developer → Planner → Architect → User) and leave an audit trail in `agentic/logs/`.
The agents are distributed as Claude Code skills (`skills/*/SKILL.md`); per-project
scaffolding lives in `templates/`.

---

## 2. Problems found

### Functional defects (the workflow does not work as advertised)

**P1 — The subagent→user channel does not exist.**
The README and `architect/SKILL.md` promise that an Architect spawned two levels deep
(Developer → Planner → Architect) "asks the user" when context is insufficient. In Claude
Code, subagents launched via the Agent tool run non-interactively: they have no
`AskUserQuestion`, and their output returns only to the spawner. The promised escalation
path is impossible as designed.

**P2 — Spawned subagents never load their own SKILL.md.**
Developer spawns the "Planner" as `subagent_type="general-purpose"` with a ~10-line inline
prompt (`developer/SKILL.md`), and Planner spawns the "Architect" the same way
(`planner/SKILL.md`). Neither prompt tells the subagent to read its skill file. The spawned
agent is an impoverished copy that lacks the full decision authority rules, log formats, and
escalation criteria — and the inline copies will drift from the SKILL.md files over time.

**P3 — The AGENT_LOG protocol contradicts itself.**
(a) `templates/AGENT_LOG.md` declares the file append-only ("Do not edit past entries"),
but `developer/references/formats.md` says the Planner *fills in remaining fields* of the
Developer's pre-call entry — an edit of a past entry.
(b) Field names disagree: the Developer pre-call format uses **What I established**, the
Planner format uses **Reasoning**, and the README example mixes both.
(c) DEC-NNN IDs are assigned by both Developer (pre-call) and Planner ("increment from
the last entry"), so nested or parallel calls can collide.

**P4 — CLARIFICATIONS.md is never written by anyone.**
`templates/CLAUDE.md` lists Planner/Developer as its writers and the Architect reads it at
startup and during reviews — but neither `planner/SKILL.md` nor `developer/SKILL.md`
contains any instruction about when or how to write it. In practice the file stays empty
forever.

### Design gaps (the workflow works, but poorly, on complex projects)

**P5 — Tasks are not self-contained.**
A task is one line (`TASK-NNN: description + files`). Execution only works because the
Developer holds the entire project in context. This blocks fresh-context execution,
cheaper-model execution, and any meaningful per-task verification.

**P6 — No independent verification; the Developer grades its own work.**
The Developer writes the code and (implicitly) the tests, so both embody the same
interpretation of the blueprint. A misread spec produces green tests and wrong behavior.
There is no actor with an independent reading of the contract.

**P7 — No component isolation strategy.**
Phases are organized by feature, not by component. There is no convention for stubs/fakes,
no per-component acceptance gate, and no explicit final integration phase. On complex
projects, everything is first tested end-to-end, which is the most expensive place to find
a defect.

**P8 — Context rot in long Developer sessions.**
A single monolithic Developer accumulates context across many tasks. Late-session work
degrades, and accumulated (possibly wrong) interpretations are never flushed.

### Minor issues

**P9 —** Task ID numbering convention (001/010/100) is implicit and collides past 9 tasks
per phase; `ln -s` install fails on re-run (`ln -sfn`); the decision-authority matrix is
duplicated between README and three SKILL.md files with no sync mechanism; no `examples/`
directory demonstrating a real session; no CI (markdown lint / link check); hero image has
a sloppy alt text.

---

## 3. Redesign decisions

### Escalation and logging mechanics

**D1 — Structured escalation instead of direct user access.**
A blocked subagent returns a structured result `NEEDS_USER_INPUT: <question + context>`
to its spawner. The sentinel propagates up the chain to the top-level agent (the only one
in session with the user), which asks via AskUserQuestion, then re-spawns the subagent
with the answer included. Fixes P1. All spawn-prompt templates and
`architect/SKILL.md` §"When Invoked as Subagent" are rewritten around this contract.
The same mechanism, with sentinel `NEEDS_DECISION`, is used by task executors toward the
Developer orchestrator (see D7).
Complete rewrite list (per review Q1 — every place that asserts the impossible path):
the two spawn-prompt templates; `architect/SKILL.md` §"When Invoked as Subagent"; the
README mermaid diagram (both "needs user input" arrows); README §"The Three Agents"
("Always asks the user … even when spawned as a subagent"); `developer/SKILL.md`
§"AskUserQuestion — last resort" (reworded to the sentinel contract).

**D2 — Spawn prompts load the skill file.**
Every spawn prompt begins with "Read `<skills-path>/<agent>/SKILL.md` and follow it",
keeping only question-specific context inline. Fixes P2.

**D3 — AGENT_LOG is strictly append-only with a single ID assigner.**
The Developer's pre-call entry carries no Decision ID and no fields "to be filled".
The responder (Planner or Architect) appends a *separate* response entry, assigns the
DEC-NNN, and references the question entry by timestamp. Field names are unified
(**Reasoning** everywhere; the pre-call entry keeps **What I established** as its own
field, never merged). Fixes P3.
Concurrency rule (review Q2): log-writing subagent calls are **strictly sequential** —
never run two concurrently; IDs are not namespaced. In the two-hop case
Developer → Planner → Architect, the Architect appends its own response entry with its
own DEC, and the Planner's response entry references it: two entries, two IDs, appended
in completion order.

**D4 — CLARIFICATIONS.md gets an owner.**
The Planner writes a CLR entry whenever it resolves an interpretive ambiguity without a
blueprint change (whether invoked directly or as a subagent). The Architect remains the
reader/consolidator. Fixes P4.

### Task format: self-contained work orders

**D5 — Tasks become work orders in one file each.**
`TASKS.md` remains the index/checklist; full task definitions move to
`agentic/plan/tasks/TASK-NNN.md`. A fresh executor reads exactly one file. Required fields:

- **Componente / Goal** — one sentence
- **Contract** — 3–4 line inline summary + pointer to blueprint sections (see D6)
- **Read first** — explicit file/section manifest
- **Modify** — files to create or change
- **Environment** — how to run the acceptance commands (setup steps, working directory,
  env vars); a weak executor must not have to discover this
- **Workspace preconditions** — what earlier tasks already created that this task relies on
- **Acceptance criteria** — machine-checkable where possible (commands that must pass)
- **Do not** — explicit boundaries (interfaces not to touch, no new dependencies, …)
- **If unspecified** — explicit escalation triggers: "if X is ambiguous, return
  NEEDS_DECISION; do not improvise"
- **Executor tier** — model tier for this task, set by the Planner (see D11)
- **Execution mode** — `executor` (default) or `operator` (see D13)
- **Human review** — `human_review_required: true|false` (see D13)
- **Docs to update** — optional; mandatory when the project has a doc-contract that
  treats staleness as a defect

Fixes P5. The "Do not" and "If unspecified" sections exist specifically to make execution
safe for weaker models, which fail more by overreach and by guessing than by inability.
Rule for the Planner: a task specifies *contract and boundaries*, never the implementation
— a task that contains prose-code is a planning defect.

**D6 — Contract representation: pointer + summary, blueprint wins.**
Full inlining goes silently stale when blueprints are updated mid-implementation (which
the workflow explicitly supports); a bare pointer forces weak executors to digest whole
blueprints. Decision: short inline summary for orientation + pointer as the source of
truth, with the rule "if summary and blueprint disagree, the blueprint wins — and report
the mismatch". This doubles as a free drift detector.

### Execution model: orchestrator + fresh executors

**D7 — The Developer becomes an orchestrator.**
For each task it spawns a fresh **executor** subagent with the work-order file and a short
**conventions brief**. The orchestrator never reads implementation code — one narrow
exception (review §3.5, option b): it may read interface/signature lines strictly to
patch a downstream work order, never implementation bodies. It reads TASKS.md,
dispatches, collects a structured summary, updates TASKS/DEVLOG, and moves on. Executor
return format includes an **impacts** field: anything that affects downstream tasks
(changed interface, new file, deviation). On impacts, the orchestrator patches downstream
work orders or spawns the Planner to re-plan. Blocked executors return `NEEDS_DECISION`;
the orchestrator routes to Planner (→ Architect → user per D1) and re-spawns the executor
with the answer. Fixes P8; enables cheap-model execution (see D11).
**Partial-work protocol** (review §3.1): work orders instruct executors to escalate
*before* modifying files whenever the ambiguity is detectable up front (that is what the
"If unspecified" triggers are for); when a mid-work block is unavoidable, the
`NEEDS_DECISION` return must include a workspace-state summary (files touched, state of
each), and the orchestrator includes it in the re-spawn prompt.
**Conventions brief contents** (review §4.2): DEC decisions relevant to the component,
doc-contract obligations, naming/test conventions observed so far. Hard cap ~half a page
so it does not become a second context-rot vector.

**D8 — Per-task mechanical check (not an agent).**
Before marking a task `[x]`, the orchestrator runs the machine-checkable acceptance
commands listed in the work order (e.g., `pytest …` exits 0). No LLM judgment involved;
near-zero cost. Catches "executor claims done but tests fail" at the task, not at the gate.
After the check passes, the orchestrator **commits the task** (task ID in the commit
message). Cheap executors with no VCS checkpoints is the riskiest combination in the
design; per-task commits make every executor mistake cheaply revertible.

### Testing and verification

**D9 — Test ownership is split three ways.**
- **Planner** specifies acceptance criteria (the *what*) at planning time, derived from
  blueprints. Spec-level bias surfaces at plan approval, where the user can see it.
- **Developer executor** writes white-box unit tests while implementing — it needs them
  for its own loop; these share its interpretation by design and that is acceptable.
- **Verifier** (new agent) writes and runs **black-box contract tests** from blueprint +
  acceptance criteria at the end of each component phase. It must NOT read the
  implementation internals, the executor's tests, or the DEVLOG — it reads the contract,
  not the process. It derives tests from the blueprint *first*, then checks criteria
  coverage, so it can also catch Planner gaps. Verifier failures come back to the
  orchestrator as new fix tasks executed by a fresh executor — the author never defends
  its own code. Fixes P6.

Hard rules to be written into the Verifier and orchestrator skill files (review Q4 and
§3.6 — rules in prose or risk tables don't execute):
1. Derive tests from the blueprint **before** reading the Planner's acceptance criteria;
   use the criteria as a coverage checklist afterwards.
2. Explicit **Do not read** block: implementation internals, executor tests, DEVLOG.
3. At most **2 fix rounds per gate**; a third failure escalates to the Planner as a
   design/planning defect, not a coding defect.

Honesty note (goes in the README): two LLM actors share training priors — the Verifier
reduces correlated misreading, it does not eliminate it. The mechanical checks (D8) and
the user's plan-approval gate are the only fully independent verdicts.

**D10 — Component-phased planning with an integration endgame.**
Planner organizes phases per component, dependency-ordered. Unbuilt dependencies are
replaced by stubs/fakes planned as explicit tasks. The last task of every component phase
is the gate: "component contract tests green in isolation" (Verifier run). The final phase
is integration: replace fakes with real components, add end-to-end tests. Fixes P7.
Concretized per review Q5:
1. Fakes implement the blueprint interface **exactly** (same signatures, same schemas),
   live in a dedicated `tests/fakes/`, and are written as explicit tasks.
2. Integration tests are specified by the **Planner at planning time** (as tasks with
   acceptance commands), never improvised during the endgame.
3. Fake retirement is an explicit task per dependency ("replace FakeX with X; delete
   FakeX; integration tests green").
4. The component gate is a named command ("`pytest tests/contract/test_<component>.py`
   exits 0"), not a sentence.

**D11 — Model tiering, per task (not per role).**
Strong models where judgment concentrates: Architect, Planner, Verifier, and the
orchestrator. Cheaper models (via the Agent tool `model` parameter) for task executors —
safe because work orders carry explicit boundaries, machine-checkable criteria, and
escalation triggers (D5). The Verifier is the last place to save money: finding what is
wrong takes more judgment than implementing.
Tiering is set **per work order** by the Planner via the Executor tier field (review
§3.2). Rule of thumb: if the acceptance criteria fully pin the behavior, tier down; if
correctness requires judgment the criteria cannot capture (statistical logic, prompt
engineering, numerically subtle code), tier up. The cheap default applies only where the
work order says so.

**D12 — Verifier exposure.**
Spawned automatically by the orchestrator at component gates, and also available as a
manual `/verifier` skill for on-demand audits of an existing component. It is a service
agent, not a fourth stage in the main pipeline.

**D13 — Execution modes and by-design human checkpoints.**
Work orders carry an **Execution mode**: `executor` (default — fresh spawned subagent) or
`operator` — tasks needing live API keys, paid third-party services, or 30+ minute
external runs are surfaced by the orchestrator to the top-level session/user instead of
spawned (subagents would hit timeouts and cannot be interactive). Separately, a
`human_review_required: true` flag pauses the orchestrator after the task until the user
has reviewed the produced artifact (e.g., a trust-anchor file consumed by downstream
tasks, agent-protected afterwards). This is a *by-design blocking* interaction, distinct
from the exceptional `NEEDS_USER_INPUT` escalation. Both driven by the first consumer
project's requirements (review §5).

**D14 — Task bundling instead of orchestrator inline execution.**
Cost control for trivial tasks (review §3.3) is solved at plan time: the Planner may
bundle small, same-component, same-files tasks into one work order. The alternative — an
orchestrator size threshold for executing trivial tasks directly — was rejected because
it would re-introduce source code, and therefore context rot, into the long-lived
orchestrator, which D7 exists to prevent. Runtime-generated fix tasks (from Verifier
failures) always go to a fresh executor, however small.

---

## 4. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Planner becomes the bottleneck; work orders are expensive to write | Run Planner on a strong model; plan-approval gate with the user becomes the main QC point; "contract and boundaries, never implementation" rule keeps tasks from bloating into prose-code |
| Work orders go stale as upstream tasks deviate | Executor **impacts** field + orchestrator patches downstream tasks or re-plans (D7); blueprint-wins rule (D6) |
| Weak executors improvise instead of escalating | Escalation triggers written *inside each task* (D5), not only in the skill |
| Verifier loop never converges (fix → fail → fix) | Hard rule in the Verifier and orchestrator skill files (D9): cap 2 rounds per gate; third failure escalates to Planner as a planning/design defect |
| Executor escalates mid-task with files already modified | Partial-work protocol (D7): escalate before modifying when detectable; otherwise workspace-state summary in the NEEDS_DECISION return |
| Cheap executor on a judgment-dense task produces plausible-wrong code | Per-task tiering set by the Planner (D11) |
| README ↔ SKILL.md duplication drifts | Declare README non-normative, or add a release checklist / CI consistency check |

---

## 5. Implementation phases

- **Phase 0 — Mechanical fixes and doc sync** (D1–D4). Full scope (review §3.4): the
  D1 rewrite list (spawn templates, architect SKILL, README diagram + "The Three Agents"
  text, developer "AskUserQuestion" section); `templates/CLAUDE.md` key-files table
  (CLARIFICATIONS writer → Planner only) and rule 6 (reworded to the new question-entry
  format); `templates/AGENT_LOG.md` comment block split into question-entry and
  response-entry formats; one line in the README declaring the SKILL.md files normative
  and the README descriptive. **Definition of done: no document in the repo asserts a
  behavior the mechanics make impossible, and no two documents disagree on a format.**
- **Phase 1 — Planner upgrade** (D5, D6, D10, D13 fields, D14 bundling + Architect:
  testable contracts in blueprints, acceptance examples in the API section).
- **Phase 2 — Developer orchestrator** (D7, D8, D11, D13 modes; per-task commits).
- **Phase 3 — Verifier** (D9, D12, including the hard rules and round cap as skill text).
- **Phase 4 — Portfolio polish** (P9: CI lint, README fixes, install script with
  `ln -sfn`). The `examples/` directory is produced by running the upgraded workflow
  end-to-end on a small real project — this validates Phases 0–3 and closes the examples
  gap in one move (review §4.3).

Ordering: Phase 1 is a prerequisite of 2 and 3. Phase 0 is independent and can ship
first. Per the review's sequencing opinion: Phases 0–2 are sufficient for the first
consumer project (digital-twin-pipeline) to begin under the new workflow; Phase 3 can
land during its first component phase and apply from the first gate onward; Phase 4 must
not delay anything.

---

## 6. What a reviewing agent should check

> **Resolved:** all six questions were answered in `IMPROVEMENT_REVIEW.md` §2 and the
> resulting changes are folded into §3–§5 above. Kept for the record.

1. Does D1 actually close P1 — i.e., is there any remaining path where a subagent is
   expected to reach the user directly?
2. Is the D3 logging protocol free of write conflicts under nested calls
   (Developer → Planner → Architect), and is the DEC assigner unambiguous?
3. Is the D5 work-order format sufficient for a *weaker* model to execute without reading
   anything outside its manifest? What is missing?
4. Does the D9 split genuinely break the self-grading loop, or can bias leak through the
   Planner's acceptance criteria into both Dev and Verifier? Is the "blueprint-first"
   instruction to the Verifier enough?
5. Is the integration phase (D10) specified concretely enough to be planned, or is
   "replace fakes with real components" hand-waving?
6. Are there contradictions between this report and the current SKILL.md/templates that
   Phase 0–3 do not explicitly resolve?
