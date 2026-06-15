# Counter Blueprint

**Component:** counter
**Version:** 1.0

## 1. Scope

Given a list of tokens, returns a frequency map and a top-N view. Depends on the
**tokenizer** interface (not its implementation) — develops against `FakeTokenizer`
until the integration phase.

## 2. API / Interface

```python
def count_frequencies(tokens: list[str]) -> dict[str, int]: ...

def top_n(tokens: list[str], n: int) -> list[tuple[str, int]]: ...
```

- `count_frequencies`: occurrence count per token; empty list → empty dict.
- `top_n`: the `n` most frequent tokens, ties broken by first-occurrence order,
  truncated to the available count; `n <= 0` → empty list.

**Acceptance examples:**

| Call | Result | Note |
|------|--------|------|
| `count_frequencies(["a","b","a"])` | `{"a": 2, "b": 1}` | |
| `count_frequencies([])` | `{}` | empty in, empty out |
| `top_n(["a","b","a","c","b","b"], 2)` | `[("b", 3), ("a", 2)]` | ties by insertion order |
| `top_n(["a"], 0)` | `[]` | non-positive n |

## 3. Data structures

Plain `dict[str, int]` and `list[tuple[str, int]]`. Token identity is the string value.

## 4. Architectural decisions

1. **Depend on the tokenizer's interface, not its module.** Counter accepts
   `list[str]`; it never imports tokenizer. This is what lets it develop against a fake.
2. **Deterministic tie-breaking** by first-occurrence order, so `top_n` is reproducible
   and testable without sorting ambiguity.

## 5. Dependencies

The tokenizer's *contract* (§2 of TOKENIZER_BLUEPRINT.md) — satisfied by
`tests/fakes/fake_tokenizer.py` during development, by the real tokenizer at integration.

## 6. Out of scope for V1

- Weighted frequencies, n-grams, or co-occurrence.
- Persistence / caching of counts.
