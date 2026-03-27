# agentic-dev-workflow

A three-agent development workflow for Claude Code: **Architect → Planner → Developer**.

The Architect designs. The Planner plans. The Developer implements — spawning the others as subagents when blocked, without interrupting the user unless truly necessary.

---

## Philosophy

Most AI-assisted development fails at scale because the agent either:
- Asks the user too many questions (constant interruptions)
- Makes too many decisions alone (diverges from intent)

This workflow solves it with a **decision authority matrix**: each agent knows exactly which decisions it owns, which to delegate up the chain, and when (rarely) to ask the user.

The user interacts primarily with the **Architect** (design phase) and the **Developer** (implementation phase). The Planner is mostly invisible — spawned on demand as a subagent.

---

## The Three Agents

### Architect
**When:** Project start, major redesign, or when a blueprint needs updating.
**What it produces:** `*_BLUEPRINT.md` files — scope, API contracts, data structures, architectural decisions.
**Interaction style:** Asks focused questions, waits for confirmation before writing. Never proceeds without user sign-off on major decisions.

### Planner
**When:** After blueprints are finalized, before implementation begins. Also spawned on-demand by Developer.
**What it produces:** `DEVELOPMENT_PLAN.md`, `TASKS.md`.
**Interaction style:** Mostly autonomous. Escalates to Architect subagent when blueprint gaps arise. Only reaches the user if genuinely blocked.

### Developer
**When:** During implementation.
**What it does:** Reads TASKS.md, implements sequentially, marks tasks complete, logs everything.
**Interaction style:** Autonomous. Spawns Planner subagent when blocked. Uses `AskUserQuestion` only as a last resort.

---

## Decision Authority Matrix

| Decision type | Developer alone | → Planner | → Architect | → User |
|--------------|:-:|:-:|:-:|:-:|
| Implementation details within a function | ✓ | | | |
| New file/module not in the plan | | ✓ | | |
| API contract change | | ✓ | | |
| New dependency | | ✓ | | |
| Blueprint ambiguity (resolvable from context) | | ✓ | | |
| Conflicting requirements between blueprints | | | ✓ | |
| New requirement not in any blueprint | | | ✓ | |
| Product/business judgment | | | | ✓ |
| Security/compliance decision | | | | ✓ |

---

## Installation

Symlink the skill directories to your Claude Code skills directory (symlinks mean edits to this repo are reflected immediately):

```bash
mkdir -p ~/.claude/skills

ln -s $(pwd)/skills/architect ~/.claude/skills/architect
ln -s $(pwd)/skills/planner   ~/.claude/skills/planner
ln -s $(pwd)/skills/developer ~/.claude/skills/developer
```

Verify with `/help` in Claude Code — the three skills should appear in the list.

---

## Starting a New Project

**Step 1 — Design**

```
/architect
```

The Architect reads your existing files and asks questions. Answer them. When done, it writes the blueprint files. Repeat until the design is solid.

**Step 2 — Plan**

```
/planner
```

The Planner reads the blueprints and produces `DEVELOPMENT_PLAN.md` and `TASKS.md`. Review them. Adjust if needed.

**Step 3 — Implement**

```
/developer
```

The Developer picks up `TASKS.md` and implements. It will spawn Planner (and Architect) subagents autonomously when blocked. You only get interrupted if the agents can't resolve something.

---

## Project Files

Copy templates to your project root:

```bash
cp templates/DEVELOPMENT_PLAN.md  your-project/
cp templates/TASKS.md             your-project/
cp templates/AGENT_LOG.md         your-project/
cp templates/DEVIATIONS.md        your-project/
cp templates/CLARIFICATIONS.md    your-project/
cp templates/CLAUDE.md            your-project/   # rename/merge with existing CLAUDE.md
```

---

## Inter-Agent Conversation Logging

All decisions made between agents are logged in `AGENT_LOG.md`. This provides a full audit trail of why implementation choices were made — useful for liability, onboarding new team members, and debugging divergence from blueprints.

`DEVIATIONS.md` records every case where the implementation differs from what the blueprint specified.

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
    DEVELOPMENT_PLAN.md
    TASKS.md
    AGENT_LOG.md
    DEVIATIONS.md
    CLARIFICATIONS.md
    CLAUDE.md                   ← project CLAUDE.md template
```
