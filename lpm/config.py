DEFAULT_CONFIG = {}


class Config:
    INIT = False
    CONFIG_PATH = None
    "Path to configuration file."

    TAB_SPACES = None
    COLOR = None
    COLOR_FOREGROUND = None
    COLOR_BACKGROUND = None
    COLOR_STATS = None
    COLOR_INFO = None
    COLOR_TEXT = None
    COLOR_CORRECT = None
    COLOR_INCORRECT = None
    MAX_LINES = None
    MAX_CHARS = None

    @staticmethod
    def load():
        pass

    @staticmethod
    def reset():
        pass


if not Config.init:
    Config.load()
    Config.init = True
