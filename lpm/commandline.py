"""Module that specifies the lpm command-line interface.

Use `lpm -h` for help.
"""

import os
import argparse

from . import __version__
from .config import Config
from .snippets import Snippets
from .stats import Stat, Stats
from .game import Game


def stats():
    """Displays the users statistics to the command-line.

    This method outputs text to the command-line.
    """
    # TODO: make this better
    # TODO: only show last N things
    if not os.path.exists(Config.STATS_PATH):
        print("No stats recorded")
    else:
        from datetime import datetime, timedelta

        statistics = Stats.load(Config.STATS_PATH)

        lifetime = Stat()
        elapsed = 0
        i = len(statistics)
        print("last 5 games")
        print("------------")
        for s in statistics:
            lifetime.num_chars += s.num_chars
            lifetime.num_lines += s.num_lines
            lifetime.num_correct += s.num_correct
            lifetime.num_wrong += s.num_wrong
            elapsed += s.elapsed
            if i <= 5:
                print(s.end_time.strftime("%Y-%m-%d %H:%M:%S"), "  ", s)
            i -= 1

        lifetime.start_time = datetime.today()
        lifetime.end_time = lifetime.start_time + timedelta(0, elapsed)
        print("")
        print("lifetime stats")
        print("--------------")
        print(
            f"{len(statistics)} games | {lifetime.elapsed:.2f}s total elapsed | "
            "{lifetime.lpm:.2f} avg lpm | {lifetime.wpm:.2f} avg wpm | "
            "{lifetime.cpm:.2f} avg cpm | {lifetime.acc*100:.2f}% avg acc"
        )


def start(languages=None):
    """Starts the lpm typing interface.

    Parameters
    ----------
    languages : list[str]
        Whitelist of programming languages to load code snippets for.
    """
    if not languages:
        languages = Config.DEFAULT_LANGS
    for lang in languages:
        if lang.lower() not in Config.DEFAULT_LANGS:
            print(
                "ERROR: one or more args are not valid languages, must be one of:\n",
                ", ".join(Config.DEFAULT_LANGS),
            )
            return

    # load snippets
    if not os.path.exists(Config.SNIPPETS_PATH):
        from . import _github_permalink

        print("... downloading snippets ...")

        snippets = Snippets.from_urls(_github_permalink)
        snippets.save(Config.SNIPPETS_PATH)
    snippets = Snippets.load(Config.SNIPPETS_PATH, languages=languages)

    # load stats
    if not os.path.exists(Config.STATS_PATH):
        statistics = Stats([])
    else:
        statistics = Stats.load(Config.STATS_PATH)

    with Game(snippets, statistics) as game:
        game.run()


def settings():
    """Allows user to modify lpm settings through their text editor.

    This method will open the config file using the default text editor, thus
    replacing the command line window.
    """
    editor = os.environ.get("EDITOR", "vim")
    os.system(f"{editor} {Config.CONFIG_PATH}")


def reset():
    """Resets the settings for lpm.

    This method can update both the config and stats files, based on user choice.
    """
    config_reset = input("Do you want to reset your config? (y/n): ")
    if config_reset.lower() == "y":
        Config.reset()
        print("User settings were reset using defaults.\n")

    stats_reset = input("Do you want to reset your lifetime statistics? (y/n): ")
    if stats_reset.lower() == "y":
        if os.path.exists(Config.STATS_PATH):
            os.remove(Config.STATS_PATH)
            print("User statistics were reset.\n")
        else:
            print("User statistics do not exist.\n")

    snippets_reset = input("Do you want to redownload snippets? (y/n): ")
    if snippets_reset.lower() == "y":
        from . import _github_permalink

        print("... downloading snippets ...")

        snippets = Snippets.from_urls(_github_permalink)
        snippets.save(Config.SNIPPETS_PATH)

        print("... done ...")


def cli():
    """Main entry point for lpm CLI."""
    parser = argparse.ArgumentParser(
        "lpm",
        description="Lines Per Minute, a typing tool made for programmers.",
        epilog="Example usage:\n"
        "    lpm\n"
        "    lpm python\n"
        "    lpm java\n"
        "    lpm python java\n"
        "    lpm --help\n"
        "    lpm --stats\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "languages",
        type=str,
        default=Config.DEFAULT_LANGS,
        nargs="*",
        help="List of programming languages to filter code snippets. Must be "
        f"one of a {', '.join(Config.DEFAULT_LANGS)}. If no languages provided, "
        "all languages are loaded by default.",
    )
    parser.add_argument(
        "-s",
        "--stats",
        action="store_true",
        help="Display the lifetime statistics and the statistics from the 5 "
        "most recent completed snippets.",
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Get program version."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Prompts the user if they would like to reset the config, stats, "
        "and/or redownload the code snippets.",
    )
    parser.add_argument(
        "--settings",
        action="store_true",
        help="Edit lpm settings via default text editor.",
    )

    args, unknown = parser.parse_known_args()
    if unknown:
        print("ERROR: invalid flag(s), please see lpm -h for more info")
    elif args.stats:
        stats()
    elif args.version:
        print(__version__)
    elif args.reset:
        reset()
    elif args.settings:
        settings()
    else:
        start(args.languages)
