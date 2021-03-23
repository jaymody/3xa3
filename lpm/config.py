"""Module that handles lpm configuration.

This module handles app configurations that can be modified by the user. The
configuration is loaded from CONFIG_PATH, which the user may edit via:
`lpm --settings`
"""

import os
import json

DEFAULT_CONFIG = {
    "CONFIG_PATH": "~/.lpmconfig.json",
    "COLOR": "#5f85c0",
    "COLOR_BACKGROUND": "#121212",
    "COLOR_STATS": "#77abfc",
    "COLOR_INFO": "#77abfc",
    "COLOR_TEXT": "#5f85c0",
    "COLOR_CORRECT": "#9effb6",
    "COLOR_INCORRECT": "#da5a58",
    "STATS_PATH": "~/.lpmstats.pickle",
    "SNIPPET_PATH": "~/.lpmsnippets.pickle",
    "DEFAULT_LANGS": ["python", "java", "javascript"],
    "MAX_LINES": 24,
    "MAX_COLS": 80,
}

"""Stores the default configuration for lpm."""


class Config:
    """App configuration loaded from CONFIG_PATH.

    Examples
    --------
    from Config import Config

    Config.BACKGROUND_COLOR
    """

    INIT = False
    "Flag that stores if the config has been loaded."

    CONFIG_PATH = os.path.expanduser(DEFAULT_CONFIG["CONFIG_PATH"])
    "Path to configuration file."

    STATS_PATH = os.path.expanduser(DEFAULT_CONFIG["STATS_PATH"])
    "Path to stats file."

    SNIPPETS_PATH = os.path.expanduser(DEFAULT_CONFIG["SNIPPET_PATH"])
    "Path to snippets file."

    COLOR = DEFAULT_CONFIG["COLOR"]
    "Highlight color, used for stats header color."

    COLOR_BACKGROUND = DEFAULT_CONFIG["COLOR_BACKGROUND"]
    "Background color."

    COLOR_STATS = DEFAULT_CONFIG["COLOR_STATS"]
    "Color of stats text."

    COLOR_INFO = DEFAULT_CONFIG["COLOR_INFO"]
    "Color of snippet information text (author, title, etc...)."

    COLOR_TEXT = DEFAULT_CONFIG["COLOR_TEXT"]
    "Color of snippet text."

    COLOR_CORRECT = DEFAULT_CONFIG["COLOR_CORRECT"]
    "Color of snippet text that was correctly typed."

    COLOR_INCORRECT = DEFAULT_CONFIG["COLOR_INCORRECT"]
    "Color of snippet text that was incorrectly typed."

    DEFAULT_LANGS = DEFAULT_CONFIG["DEFAULT_LANGS"]
    "Code snippet programming languages to load lpm with by default."

    MAX_LINES = DEFAULT_CONFIG["MAX_LINES"]
    """Max lines allowed for a code snippet."""

    MAX_COLS = DEFAULT_CONFIG["MAX_COLS"]
    """Max cols allowed for a code snippet."""

    @staticmethod
    def load():
        """Loads the configuration file from CONFIG_PATH."""
        # reset if file does not exist
        #
        # if config_path is invalid json or some field is missing
        # report error to user (ask them to verify or ask them to lpm --reset)
        ignore = {"CONFIG_PATH", "STATS_PATH", "SNIPPETS_PATH"}
        if not (os.path.exists(Config.CONFIG_PATH)):
            Config.reset()
        else:
            with open(Config.CONFIG_PATH) as fi:
                data = json.load(fi)
                for k, v in data.items():
                    if k in DEFAULT_CONFIG and k not in ignore:
                        setattr(Config, k, v)

    @staticmethod
    def reset():
        """Resets the configuration file to DEFAULT_CONFIG."""
        with open(Config.CONFIG_PATH, "w") as fo:
            fo.write(json.dumps(DEFAULT_CONFIG, indent=4))


# loads the Config file if it hasn't been loaded yet
# this runs when config is imported
if not Config.INIT:
    Config.load()
    Config.INIT = True
