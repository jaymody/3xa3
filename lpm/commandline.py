"""Module that specifies the lpm command-line interface.

Use `lpm -h` for help.
"""

import argparse


def stats():
    """Displays the users statistics to the command-line."""
    print("pi = 3.14")
    # display lifetime stats
    pass


def start():
    """Starts the lpm typing interface."""
    # load stats
    # load snippets
    # load screen
    # create game
    try:
        # game.run()
        pass
    except KeyboardInterrupt:
        # save stats, clear screen or something, quit game
        pass


def settings():
    """Allows user to modify lpm settings."""
    # open vim with CONFIG_PATH
    pass


def reset():
    """Resets the settings for lpm."""
    # ask if they want to reset config (y/n), call Config.reset
    # ask if they want to delete stats (y/n) delete the stats file
    pass


def cli():
    """Main entry point for lpm CLI."""
    parser = argparse.ArgumentParser("Lines Per Minute")
    parser.add_argument("--stats", action="store_true")
    args = parser.parse_args()

    if args.stats:
        stats()
