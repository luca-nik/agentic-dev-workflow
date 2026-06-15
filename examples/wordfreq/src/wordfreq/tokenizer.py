"""Tokenizer — splits and normalizes a string into tokens.

Contract source of truth: agentic/blueprints/TOKENIZER_BLUEPRINT.md §2.
- casefold each token (CLR-001)
- non-alphanumeric characters separate (DEC-001: apostrophes separate)
- plain str tokens, no offsets (DEV-001)
"""


def tokenize(text: str) -> list[str]:
    """Split ``text`` into an ordered list of case-folded tokens.

    Raises TypeError if ``text`` is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    token: list[str] = []
    out: list[str] = []
    for ch in text:
        if ch.isalnum():
            token.append(ch)
        elif token:
            out.append("".join(token).casefold())
            token = []
    if token:
        out.append("".join(token).casefold())
    return out
