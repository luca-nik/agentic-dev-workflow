# Deviations — wordfreq

Records every case where the implementation differs from what the blueprint specifies.

Deviations are not failures — they are information. A deviation documents that the
blueprint was wrong, incomplete, or that reality differed from the design assumption.
This file is used to update blueprints in the next planning cycle.

This file is append-only. Do not edit past entries.

---

## DEV-001 — 2026-06-14

**Task:** TASK-001
**Blueprint says:** TOKENIZER_BLUEPRINT.md v1.0 §3 originally specified tokens as a
`Token` dataclass carrying `.text` and `.offset` (character offset of the token start).
**Implemented:** Tokens are plain `str`; no offset metadata is produced.
**Reason:** The counter (the sole V1 consumer, per COUNTER_BLUEPRINT.md §3) consumes
only token identity — it never reads offsets. Carrying offsets added complexity and a
data type with no V1 consumer. Raised as NEEDS_DECISION; Planner approved dropping
offsets in V1 (DEC-002) and §3 + §6 of the blueprint were updated to "plain `str`;
offsets out of scope for V1."
**Decision ID:** DEC-002
