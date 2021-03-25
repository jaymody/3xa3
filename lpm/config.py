"""Module that handles lpm configuration.

This module handles app configurations that can be modified by the user. The
configuration is loaded from CONFIG_PATH, which the user may edit via:
`lpm --settings`
"""

import os
import json
import curses

# TODO: either don't load snippets longer than max_lines, or base it off of the
# size of the terminal
# TODO: add multiple theme options (including one that supports non-256 terms)
# TODO: don't save stuff to home dir except .lpmconfig (rename to .lpmrc)
DEFAULT_CONFIG = {
    "CONFIG_PATH": "~/.lpmconfig.json",
    "STATS_PATH": "~/.lpmstats.pickle",
    "SNIPPET_PATH": "~/.lpmsnippets.pickle",
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

    CONFIG_PATH = os.path.expanduser(DEFAULT_CONFIG["CONFIG_PATH"])
    "Path to configuration file."

    STATS_PATH = os.path.expanduser(DEFAULT_CONFIG["STATS_PATH"])
    "Path to stats file."

    SNIPPETS_PATH = os.path.expanduser(DEFAULT_CONFIG["SNIPPET_PATH"])
    "Path to snippets file."

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
