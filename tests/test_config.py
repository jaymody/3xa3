def test_reset():
    from lpm.config import Config, DEFAULT_CONFIG

    Config.reset()
    assert Config.COLORS == DEFAULT_CONFIG["COLORS"]


def test_correct_load():
    from lpm.config import CONFIG_PATH, DEFAULT_CONFIG
    import json

    with open(CONFIG_PATH) as fi:
        data = json.load(fi)
        assert data == DEFAULT_CONFIG
