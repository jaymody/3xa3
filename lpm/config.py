"""Module that handles lpm configuration.

This module handles app configurations that can be modified by the user. The
configuration is loaded from CONFIG_PATH, which the user may edit via:
`lpm --settings`
"""

import os
import json
import curses
from . import CONFIG_PATH

# TODO: either don't load snippets longer than max_lines, or base it off of the
# size of the terminal
# TODO: add multiple theme options (including one that supports non-256 terms)
# TODO: don't save stuff to home dir except .lpmconfig (rename to .lpmrc)
DEFAULT_CONFIG = {
    "DEFAULT_LANGS": ["python", "java", "javascript"],
    "MAX_LINES": 20,
    "MAX_COLS": 80,
    "COLORS": {  # tuples represent a (fg, bg) pair
        "background": [235, 235],
        "text": [252, 235],
        "correct": [243, 235],
        "incorrect": [9, 88],
        "author": [39, 235],
        "prompt": [243, 235],
        "top_bar": [254, 32],
    },
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

    COLORS = DEFAULT_CONFIG["COLORS"]
    "xterm256 colors for interface components."

    DEFAULT_LANGS = DEFAULT_CONFIG["DEFAULT_LANGS"]
    "Code snippet programming languages to load lpm with by default."

    MAX_LINES = DEFAULT_CONFIG["MAX_LINES"]
    "Max lines allowed for a code snippet."

    MAX_COLS = DEFAULT_CONFIG["MAX_COLS"]
    "Max cols allowed for a code snippet."

    @staticmethod
    def load():
        """Loads the configuration file from CONFIG_PATH.

        This method extracts information from the config file, located at
        CONFIG_PATH.
        """
        # reset if file does not exist
        #
        # if config_path is invalid json or some field is missing
        # report error to user (ask them to verify or ask them to lpm --reset)
        if not (os.path.exists(CONFIG_PATH)):
            Config.reset()
        else:
            with open(CONFIG_PATH) as fi:
                data = json.load(fi)
                for k, v in data.items():
                    if k in DEFAULT_CONFIG:
                        setattr(Config, k, v)

    @staticmethod
    def reset():
        """Resets the configuration file to DEFAULT_CONFIG."""
        with open(CONFIG_PATH, "w") as fo:
            fo.write(json.dumps(DEFAULT_CONFIG, indent=4))


# loads the Config file if it hasn't been loaded yet
# this runs when config is imported
if not Config.INIT:
    Config.load()
    Config.INIT = True
