"""Unit tests for the Snippets.py module."""
from lpm.config import Config
from lpm.snippets import Snippets, Snippet

# create folder tests/data/ and then run download.py
SNIPPETS_PATH = "tests/data/snippets.pickle"
MIN_NUM_SNIPPET = 20


# def test_from_dict():
#     d = PYTHON_DICT
#     s = Snippet.from_dict(d[1])
#     assert s.snippet_id == d[1]["snippet_id"]
#     assert s.lines == d[1]["lines"]
#     assert s.url == d[1]["url"]
#     assert s.author == d[1]["author"]
#     assert s.language == d[1]["language"]


# def test_load_python():
#     d = Snippets.load(TEST_JSON, ["python"])
#     assert len(d) == len(PYTHON_DICT)
#     for i in range(len(d)):
#         match = False
#         for j in range(len(PYTHON_DICT)):
#             if match == True:
#                 break
#             else:
#                 match = d[i] == Snippet.from_dict(PYTHON_DICT[j])


# def test_load_all():
#     d = Snippets.load(TEST_JSON)
#     DICT = PYTHON_DICT + JAVA_DICT
#     assert len(d) == len(DICT)
#     for i in range(len(DICT)):
#         assert d[i] == DICT[i]


# def test_init_Snippets():
#     d = Snippets.load(TEST_JSON, ["python"])
#     s = Snippets(d)
#     assert s.index == 0
#     for i in range(len(d)):
#         assert s.snippets[i] in d


# def test_len():
#     d = Snippets.load(TEST_JSON, ["python"])
#     s = Snippets(d)
#     assert len(s) == len(d)


# def test_get_snippets():
#     d = Snippets.load(TEST_JSON, ["python"])
#     s = Snippets(d)
#     assert s[len(d) + 1] == None


# def test_next():
#     s = Snippets(Snippets.load(TEST_JSON, ["python"]))
#     s.next_entry()
#     assert s.index == 1
#     s.next_entry()
#     assert s.index == 0


# def test_prev():
#     s = Snippets(Snippets.load(TEST_JSON, ["python"]))
#     s.prev_entry()
#     assert s.index == 1
#     s.prev_entry()
#     assert s.index == 0


""" Tests to check if code snippets are valid"""


def test_min_snippets_per_lang():
    for lang in Config.DEFAULT_LANGS:
        assert len(Snippets.load(SNIPPETS_PATH, lang)) >= MIN_NUM_SNIPPET


def test_max_line_len_per_snippet():
    snippets = Snippets.load(SNIPPETS_PATH)
    for s in snippets:
        assert len(s.lines) <= Config.MAX_LINES


def test_max_char_len_per_snippet():
    snippets = Snippets.load(SNIPPETS_PATH)
    for s in snippets:
        for line in s.lines:
            assert len(line) <= Config.MAX_COLS, s.author + " " + s.url[-10:]
