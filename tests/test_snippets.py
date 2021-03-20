from lpm.snippets import Snippets, Snippet
from lpm.config import Config

TEST_JSON = "tests/data/snippets.json"
LPM_JSON = "lpm/snippets.json"
MIN_NUM_SNIPPET = 20
MAX_LINE_LENGTH = 30
MAX_CHARACTER_LENGTH = 88
PYTHON_DICT = [
    {
        "snippet_id": 0,
        "lines": ["for i in range(20)", "time += 1"],
        "url": "github.com",
        "author": "jay",
        "language": "python",
    },
    {
        "snippet_id": 1,
        "lines": ["print('hello')", "print('hi')"],
        "url": "github.com",
        "author": "jess",
        "language": "python",
    },
]
JAVA_DICT = [
    {
        "snippet_id": 2,
        "lines": ["print('hello')", "print('hi')"],
        "url": "github.com",
        "author": "jay",
        "language": "java",
    },
    {
        "snippet_id": 3,
        "lines": ["print('hello')", "print('hi')"],
        "url": "github.com",
        "author": "jay",
        "language": "java",
    },
]

""" Unit tests for the Snippets.py module"""


def test_from_dict():
    d = PYTHON_DICT
    s = Snippet.from_dict(d[1])
    assert s.snippet_id == d[1]["snippet_id"]
    assert s.lines == d[1]["lines"]
    assert s.url == d[1]["url"]
    assert s.author == d[1]["author"]
    assert s.language == d[1]["language"]


def test_load_python():
    d = Snippets.load(TEST_JSON, ["python"])
    assert len(d) == len(PYTHON_DICT)
    for i in range(len(d)):
        match = False
        for j in range(len(PYTHON_DICT)):
            if match == True:
                break
            else:
                match = d[i] == Snippet.from_dict(PYTHON_DICT[j])


def test_load_all():
    d = Snippets.load(TEST_JSON)
    DICT = PYTHON_DICT + JAVA_DICT
    assert len(d) == len(DICT)
    for i in range(len(DICT)):
        assert d[i] == DICT[i]


def test_init_Snippets():
    d = Snippets.load(TEST_JSON, ["python"])
    s = Snippets(d)
    assert s.index == 0
    for i in range(len(d)):
        assert s.snippets[i] in d


def test_len():
    d = Snippets.load(TEST_JSON, ["python"])
    s = Snippets(d)
    assert len(s) == len(d)


def test_get_snippets():
    d = Snippets.load(TEST_JSON, ["python"])
    s = Snippets(d)
    assert s[len(d) + 1] == None


def test_next():
    s = Snippets(Snippets.load(TEST_JSON, ["python"]))
    s.next_entry()
    assert s.index == 1
    s.next_entry()
    assert s.index == 0


def test_prev():
    s = Snippets(Snippets.load(TEST_JSON, ["python"]))
    s.prev_entry()
    assert s.index == 1
    s.prev_entry()
    assert s.index == 0


""" Tests to check if code snippets are valid"""


def test_min_snippets_per_lang():
    for lang in Config.DEFAULT_LANGS:
        assert len(Snippets.load(LPM_JSON, lang)) >= MIN_NUM_SNIPPET


def test_max_line_len_per_snippet():
    s = Snippets.load(LPM_JSON)
    for i in range(len(s)):
        assert len(s[i]["lines"]) <= MAX_LINE_LENGTH


def test_max_char_len_per_snippet():
    s = Snippets.load(LPM_JSON)
    for i in range(len(s)):
        for line in s[i]["lines"]:
            assert len(line) <= MAX_CHARACTER_LENGTH
