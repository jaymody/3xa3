def test_reset():
    from lpm.config import Config

    Config.reset()
    assert Config.COLOR_CORRECT == "#9effb6"


def test_correct_load():
    from lpm.config import Config, DEFAULT_CONFIG
    import json

    with open(Config.CONFIG_PATH) as fi:
        data = json.load(fi)
        assert data == DEFAULT_CONFIG
