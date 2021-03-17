"""Module that handles lpm configuration.

This module handles app configurations that can be modified by the user. The
configuration is loaded from CONFIG_PATH, which the user may edit via:
`lpm --settings`
"""

DEFAULT_CONFIG = {}
"""Stores the default configuration for lpm."""


class Config:
    """App configuration loaded from CONFIG_PATH."""

    INIT = False
    "Flag that stores if the config has been loaded."

    CONFIG_PATH = None
    "Path to configuration file."

    COLOR = None
    "Highlight color, used for stats header color."

    COLOR_BACKGROUND = None
    "Background color."

    COLOR_STATS = None
    "Color of stats text."

    COLOR_INFO = None
    "Color of snippet information text (author, title, etc...)."

    COLOR_TEXT = None
    "Color of snippet text."

    COLOR_CORRECT = None
    "Color of snippet text that was correctly typed."

    COLOR_INCORRECT = None
    "Color of snippet text that was incorrectly typed."

    MAX_LINES = None
    "Max lines allowed per snippet."

    MAX_CHARS = None
    "Max number of characters allowed per line in a snippet."

    @staticmethod
    def load():
        """Loads the configuration file from CONFIG_PATH."""
        pass

    @staticmethod
    def reset():
        """Resets the configuration file to DEFAULT_CONFIG."""
        pass


# loads the Config file if it hasn't been loaded yet
# this runs when config is imported
if not Config.INIT:
    Config.load()
    Config.INIT = True
