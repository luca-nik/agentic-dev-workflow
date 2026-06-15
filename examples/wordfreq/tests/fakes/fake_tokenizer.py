"""FakeTokenizer — exact interface of wordfreq.tokenizer.tokenize.

Lives in tests/fakes/. Used by the counter's contract tests during Phase 2, before the
real tokenizer is wired in at integration (Phase 3). Implements the SAME signature and
a behavior sufficient to drive counter tests cases; it is NOT a correct tokenizer.

Per COUNTER_BLUEPRINT.md §4 AD-1: counter depends on the tokenizer's interface, never
its module — so swapping this fake for the real function is a one-line change.
"""

# Re-exported under the same name the counter would import, were it not interface-only.
# Kept here as a callable matching tokenize(text: str) -> list[str].


def tokenize(text: str) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    # Deterministic, simple decomposition: lowercase, treat apostrophes and commas as
    # spaces, then split on whitespace. Enough to produce tokens for counter tests.
    return text.casefold().replace("'", " ").replace(",", " ").split()
