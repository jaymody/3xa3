DEFAULT_CONFIG = {}

"""Module for loading user config

This module interfaces with config.json, the configuration file that users will
modify if they want to edit the settings of lpm. Editable settings include:
- Color
- Amount of spaces per 'tab' inputted
- Maximum lines or characters for a given snippet

"""


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
        """Loads the configuration file from config.json."""
        pass

    @staticmethod
    def reset():
        """Resets the configuration file using the DEFAULT_CONFIG constant."""
        pass


if not Config.init:
    Config.load()
    Config.init = True
