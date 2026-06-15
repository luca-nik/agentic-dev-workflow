# Clarifications — wordfreq

Records ambiguities in blueprints that were resolved during planning or development,
without requiring a blueprint change.

If a clarification reveals that the blueprint needs to be updated, update the blueprint
and note it here. If the clarification is purely interpretive (the blueprint was correct
but unclear), record it here only.

This file is append-only. Do not edit past entries.

---

## CLR-001 — 2026-06-14

**Blueprint:** TOKENIZER_BLUEPRINT.md §2 ("Lowercases") and §4 AD-1.
**Ambiguity:** "Lowercases" did not specify the mechanism. `str.lower()` leaves some
unicode uppercase letters un-folded in edge locales; `str.casefold()` is the correct
choice for case-insensitive comparison but the blueprint did not name it.
**Resolution:** Use `str.casefold()` on each joined token. This is an interpretation of
an already-correct blueprint (AD-1 says "Case-fold, don't just lowercase" and names
`casefold()`), so it is recorded here for implementers, not a blueprint change. The
acceptance example `tokenize("Été") == ["été"]` exercises it.
**Blueprint updated:** no (AD-1 already names casefold; this just records the spot it
applies — per-token, on the joined string).
**Decision ID:** none
