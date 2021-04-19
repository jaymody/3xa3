"""Unit tests for the Snippets.py module."""
from lpm import SNIPPETS_PATH
from lpm.config import Config
from lpm.snippets import Snippets

MIN_NUM_SNIPPETS = 10


def test_CS1():
    """Test that each snippet does not have more lines than MAX_LINES."""
    snippets = Snippets.load(SNIPPETS_PATH)
    for s in snippets:
        assert len(s.lines) <= Config.MAX_LINES, s.url


def test_CS2():
    """Test that each line for each snippet under MAX_COLS."""
    snippets = Snippets.load(SNIPPETS_PATH)
    for s in snippets:
        for line in s.lines:
            assert len(line) <= Config.MAX_COLS, s.url


def test_CS3():
    """Test that each language has enough code snippet."""
    for lang in Config.DEFAULT_LANGS:
        assert len(Snippets.load(SNIPPETS_PATH, [lang])) >= MIN_NUM_SNIPPETS
