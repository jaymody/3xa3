"""Lines Per Minute."""

import os

__version__ = "0.0.9"

_package_dir = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.expanduser("~/.lpmrc")
URLS_PATH = os.path.join(_package_dir, "data", "urls.txt")
STATS_PATH = os.path.join(_package_dir, "data", "stats.json")
SNIPPETS_PATH = os.path.join(_package_dir, "data", "snippets.json")
