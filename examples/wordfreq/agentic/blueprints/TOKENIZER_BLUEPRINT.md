# Tokenizer Blueprint

**Component:** tokenizer
**Version:** 1.0

## 1. Scope

Splits an input string into a normalized, ordered list of tokens for downstream
frequency counting. Lowercases via case-folding and treats any non-alphanumeric
character as a separator.

**Does NOT do:** stemming, stop-word removal, sentence segmentation, NFKD unicode
normalization (see Out of scope for V1).

## 2. API / Interface

```python
def tokenize(text: str) -> list[str]: ...
```

- Input: an arbitrary string (including empty).
- Output: tokens in first-occurrence order; empty list for an empty/whitespace string.
- Raises `TypeError` if `text` is not a `str`.

**Acceptance examples** (these are the contract the Verifier's tests are derived from):

| Input | Output | Note |
|-------|--------|------|
| `"Hello, world!"` | `["hello", "world"]` | punctuation and whitespace separate |
| `""` | `[]` | empty in, empty out |
| `"   "` | `[]` | whitespace-only |
| `"Don't"` | `["don", "t"]` | apostrophe is a separator (DEC-001) |
| `"Été"` | `["été"]` | unicode uppercased via casefold (CLR-001) |
| `None` | raises `TypeError` | non-string rejected |

## 3. Data structures

Tokens are plain `str`. No offset or position metadata is tracked in V1 (DEV-001 —
offsets were specified then dropped as unused by the counter).

## 4. Architectural decisions

1. **Case-fold, don't just lowercase.** `str.casefold()` handles unicode uppercase
   (É→é), which `.lower()` misses for some locales. Cheaper to do it once here than to
   handle case collisions in the counter.
2. **Non-alphanumeric = separator.** Simpler than a stopword/punctuation table; covers
   whitespace, punctuation, and apostrophes uniformly.
3. **Reject non-string input loudly** (`TypeError`), never silently coerce.

## 5. Dependencies

None. This is the leaf component.

## 6. Out of scope for V1

- Unicode NFKD normalization (compatibility decompositions) — accented forms may not
  collapse to their base letter.
- Streaming / generator interface — returns a concrete list.
- Token offsets / spans — see DEV-001.
