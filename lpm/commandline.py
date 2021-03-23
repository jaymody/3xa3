"""Module that specifies the lpm command-line interface.

Use `lpm -h` for help.
"""

import os
import argparse

from . import __version__
from .config import Config
from .snippets import Snippets
from .screen import Screen
from .stats import Stat, Stats
from .game import Game


def stats():
    """Displays the users statistics to the command-line."""
    # TODO: make this better
    if not os.path.exists(Config.STATS_PATH):
        print("No stats recorded")
    else:
        from datetime import datetime, timedelta

        statistics = Stats.load(Config.STATS_PATH)

        lifetime = Stat()
        elapsed = 0
        for s in statistics:
            lifetime.num_chars += s.num_chars
            lifetime.num_lines += s.num_lines
            lifetime.num_correct += s.num_correct
            lifetime.num_wrong += s.num_wrong
            elapsed += s.elapsed
            print(s.end_time.strftime("%Y-%m-%d %H:%M:%S"), "  ", s)

        lifetime.start_time = datetime.today()
        lifetime.end_time = lifetime.start_time + timedelta(0, elapsed)
        print("-" * 32)
        print(
            f"{len(statistics)} games | {lifetime.elapsed:.2f}s total elapsed | {lifetime.lpm:.2f} avg lpm | {lifetime.wpm:.2f} avg wpm | {lifetime.cpm:.2f} avg cpm | {lifetime.acc*100:.2f}% avg acc"
        )


def start():
    """Starts the lpm typing interface."""
    # load snippets
    if not os.path.exists(Config.SNIPPETS_PATH):
        from . import _github_permalink

        print("... downloading snippets ...")

        snippets = Snippets.from_urls(_github_permalink)
        snippets.save(Config.SNIPPETS_PATH)
    else:

        snippets = Snippets.load(Config.SNIPPETS_PATH)

    # load stats
    if not os.path.exists(Config.STATS_PATH):
        statistics = Stats([])
    else:
        statistics = Stats.load(Config.STATS_PATH)

    with Game(snippets, statistics) as game:
        game.run()


def settings():
    """Allows user to modify lpm settings."""
    editor = os.environ.get("EDITOR", "vim")
    os.system(f"{editor} {Config.CONFIG_PATH}")


def reset():
    """Resets the settings for lpm."""
    config_reset = input("Do you want to reset your config? (y/n) ")
    if config_reset == "y" or config_reset == "Y":
        Config.reset()
        print("User settings were reset using defaults. \n")

    stats_reset = input("Do you want to reset your lifetime statistics? (y/n) ")
    if stats_reset == "y" or stats_reset == "Y":
        if os.path.exists(Config.STATS_PATH):
            os.remove(Config.STATS_PATH)
            print("User statistics were reset. \n")
        else:
            print("User statistics do not exist. \n")


def cli():
    """Main entry point for lpm CLI."""
    parser = argparse.ArgumentParser("Lines Per Minute")
    parser.add_argument("-s", "--stats", action="store_true", help=stats.__doc__)
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show program version"
    )
    parser.add_argument("--reset", action="store_true", help=reset.__doc__)
    parser.add_argument("--settings", action="store_true", help=settings.__doc__)

    args = parser.parse_args()

    if args.stats:
        stats()
    elif args.version:
        print(__version__)
    elif args.reset:
        reset()
    elif args.settings:
        settings()
    else:
        start()
