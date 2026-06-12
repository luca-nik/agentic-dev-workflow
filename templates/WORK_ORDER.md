# TASK-NNN — [imperative title]

**Component:** [component name]
**Goal:** [one sentence]
**Executor tier:** strong | standard | economy — [one-line justification]
**Execution mode:** executor | operator
**Human review:** required | none

## Contract

[3–4 line summary of the interface/behavior this task must honor]

Source of truth: [BLUEPRINT_FILE.md §sections]. If this summary and the blueprint
disagree, the blueprint wins — report the mismatch in your result.

## Read first

- [file, or blueprint §section — the complete manifest; nothing else is assumed read]

## Workspace preconditions

- [what earlier tasks already created that this task relies on]

## Environment

[how to run the acceptance commands: setup steps, working directory, env vars]

## Modify

- [files to create or change — nothing outside this list]

## Acceptance criteria

- [ ] `[command]` exits 0
- [ ] [behavioral criterion, concrete: input X → output Y]

## Do not

- [explicit boundaries: interfaces not to touch, no new dependencies, …]

## If unspecified

- [trigger: "if X is ambiguous"] → return NEEDS_DECISION with your analysis;
  do not improvise. Escalate BEFORE modifying files when the ambiguity is
  detectable up front.

## Docs to update

- [optional; mandatory when the project has a doc-contract]
