"""Tokenizer contract tests.

Written by the Verifier (TASK-002 gate), derived from TOKENIZER_BLUEPRINT.md §2 BEFORE
consulting the work order's acceptance criteria. Exercises the public interface only.
The Verifier did not read src/wordfreq/tokenizer.py bodies, tests/unit/, or DEVLOG.md.
"""

import pytest

from wordfreq.tokenizer import tokenize


def test_punctuation_and_whitespace_separate():
    assert tokenize("Hello, world!") == ["hello", "world"]


def test_empty_string_yields_empty_list():
    assert tokenize("") == []


def test_whitespace_only_yields_empty_list():
    assert tokenize("   ") == []


def test_apostrophe_separates():  # DEC-001
    assert tokenize("Don't") == ["don", "t"]


def test_unicode_casefolded():  # CLR-001
    assert tokenize("Été") == ["été"]


def test_non_string_raises_typeerror():
    with pytest.raises(TypeError):
        tokenize(None)  # type: ignore[arg-type]
