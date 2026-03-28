# agentic-dev-workflow

A three-agent development workflow for Claude Code: **Architect → Planner → Developer**.

The Architect designs. The Planner plans. The Developer implements — spawning the others as subagents when blocked, without interrupting the user unless truly necessary.

---

## Philosophy

Most AI-assisted development fails at scale because the agent either:
- Asks the user too many questions (constant interruptions)
- Makes too many decisions alone (diverges from intent)

This workflow solves it with a **decision authority matrix**: each agent knows exactly which decisions it owns, which to delegate up the chain, and when (rarely) to ask the user.

The user interacts primarily with the **Architect** (design phase) and reviews readiness reports from **Planner** and **Developer** before each phase begins. The subagent chain resolves as much as possible before surfacing anything to the user.

---

## The Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  1. DESIGN                                                   │
│                                                             │
│  User ──► /architect                                        │
│           asks questions → writes agentic/blueprints/       │
│           user confirms each decision                       │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. PLAN                                                    │
│                                                             │
│  User ──► /planner                                          │
│           readiness check on blueprints                     │
│           gaps? ──► Architect subagent resolves             │
│           still blocked? ──► reports to user                │
│           user approves ──► writes agentic/plan/            │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. IMPLEMENT                                               │
│                                                             │
│  User ──► /developer                                        │
│           readiness check on tasks                          │
│           issues? ──► Planner subagent resolves             │
│                       (Planner may spawn Architect)         │
│           still blocked? ──► reports to user                │
│           user approves ──► implements sequentially         │
│           blocked mid-session? ──► Planner subagent         │
└─────────────────────────────────────────────────────────────┘
```

Each phase gate works the same way: **the agent surfaces, the user decides, the agent acts.** The subagent chain resolves as much as possible before reaching the user.

---

## The Three Agents

### Architect `/architect`
**Role:** Design collaborator. Discusses requirements, proposes architecture, writes blueprints.
**Produces:** `agentic/blueprints/*_BLUEPRINT.md` — scope, API contracts, data structures, architectural decisions.
**Interaction:** Asks focused questions before proposing anything. Waits for user confirmation before writing. Never proceeds on a major decision without sign-off.
**Review mode:** When asked to review, audits all blueprints for completeness and consistency, checks whether `DEVIATIONS.md` entries require blueprint updates, reports findings to user.

### Planner `/planner`
**Role:** Bridge between design and implementation. Translates blueprints into an executable plan.
**Produces:** `agentic/plan/DEVELOPMENT_PLAN.md`, `agentic/plan/TASKS.md`.
**Interaction:** Runs a readiness check on blueprints at startup — spawns Architect subagent to resolve gaps, then reports to user before planning. Also spawned on-demand by Developer when implementation hits a blocking question.

### Developer `/developer`
**Role:** Autonomous implementer. Reads tasks, writes code, logs everything.
**Produces:** Working code + `agentic/logs/DEVLOG.md` updates.
**Interaction:** Runs a readiness check on tasks at startup — spawns Planner subagent to resolve issues, then reports to user before implementing. During implementation, spawns Planner for any blocking question. Reaches the user only as a last resort.

---

## Decision Authority Matrix

| Decision type | Developer alone | → Planner | → Architect | → User |
|--------------|:-:|:-:|:-:|:-:|
| Implementation details within a function | ✓ | | | |
| New file/module not in the plan | | ✓ | | |
| API contract change | | ✓ | | |
| New dependency needed | | ✓ | | |
| Blueprint ambiguity (resolvable from context) | | ✓ | | |
| Conflicting requirements between blueprints | | | ✓ | |
| New requirement not in any blueprint | | | ✓ | |
| Product/business judgment | | | | ✓ |
| Security/compliance decision | | | | ✓ |

---

## Project Folder Structure

All workflow documents are stored in an `agentic/` folder at the project root — visible and versioned alongside the code:

```
your-project/
  agentic/
    blueprints/       ← *_BLUEPRINT.md files (written by Architect)
    plan/             ← DEVELOPMENT_PLAN.md, TASKS.md (written by Planner)
    logs/             ← AGENT_LOG.md, DEVLOG.md, DEVIATIONS.md, CLARIFICATIONS.md
  ... your source code ...
```

The agents create `agentic/` and its subdirectories automatically if they don't exist.

### What each file is for

| File | Purpose |
|------|---------|
| `agentic/blueprints/*_BLUEPRINT.md` | Architecture specs — scope, interfaces, data models, decisions |
| `agentic/plan/DEVELOPMENT_PLAN.md` | Phases, milestones, risks, open questions |
| `agentic/plan/TASKS.md` | Granular task checklist for Developer |
| `agentic/logs/AGENT_LOG.md` | Every inter-agent decision — the audit trail |
| `agentic/logs/DEVLOG.md` | Developer session log — what was implemented, what was skipped |
| `agentic/logs/DEVIATIONS.md` | Every case where implementation differed from blueprint |
| `agentic/logs/CLARIFICATIONS.md` | Blueprint ambiguities that were resolved without a blueprint change |

---

## Installation

Clone the repo and symlink the skill directories to your Claude Code skills directory:

```bash
git clone https://github.com/luca-nik/agentic-dev-workflow.git
cd agentic-dev-workflow

mkdir -p ~/.claude/skills
ln -s $(pwd)/skills/architect ~/.claude/skills/architect
ln -s $(pwd)/skills/planner   ~/.claude/skills/planner
ln -s $(pwd)/skills/developer ~/.claude/skills/developer
```

Symlinks mean any update to this repo is reflected immediately — no reinstall needed.

Verify with `/help` in Claude Code — the three skills should appear in the list.

---

## Starting a New Project

**Step 1 — Set up project files**

Copy the templates to your project root:

```bash
cp templates/CLAUDE.md your-project/CLAUDE.md   # merge with existing if needed
```

The `agentic/` folder will be created automatically by the agents.

**Step 2 — Design**

Open Claude Code in your project directory and run:
```
/architect
```
The Architect asks focused questions, then writes blueprints to `agentic/blueprints/`. Each decision requires your confirmation before being written.

**Step 3 — Plan**

```
/planner
```
The Planner checks whether the blueprints are complete enough to plan from. If there are gaps, it resolves them with an Architect subagent and reports to you. Once you approve, it produces `agentic/plan/DEVELOPMENT_PLAN.md` and `agentic/plan/TASKS.md`.

**Step 4 — Implement**

```
/developer
```
The Developer checks whether the tasks are executable, resolves issues via Planner subagent, reports to you, then implements sequentially. It spawns Planner (who may spawn Architect) for any blocker. You only get interrupted if the full chain is stuck.

---

## Audit Trail

`agentic/logs/AGENT_LOG.md` records every decision made between agents — what the question was, what was decided, who was consulted. This gives you a full audit trail of why implementation choices were made, useful for:
- Understanding why the code looks the way it does
- Onboarding new contributors
- Tracking liability when agents deviate from blueprints

`agentic/logs/DEVIATIONS.md` records every case where the implementation differed from what the blueprint specified, and why.

---

## Repository Structure

```
agentic-dev-workflow/
  README.md
  skills/
    architect/
      SKILL.md                  ← /architect skill
    planner/
      SKILL.md                  ← /planner skill
      references/formats.md     ← TASKS.md and DEVELOPMENT_PLAN.md formats
    developer/
      SKILL.md                  ← /developer skill
      references/formats.md     ← DEVLOG, AGENT_LOG, DEVIATIONS formats
  templates/
    CLAUDE.md                   ← project CLAUDE.md template
    AGENT_LOG.md
    DEVIATIONS.md
    CLARIFICATIONS.md
    DEVELOPMENT_PLAN.md
    TASKS.md
```
