"""Module that contains main logic for lpm typing game."""

from .screen import Screen
from .stats import Stat
from .config import Config


class Game:
    def __init__(self, snippets, stats):
        """Game object that runs the lpm typing game.

        Parameters
        ----------
        snippets : Snippets
            Snippets object containing database of code snippets.
        screen : Screen
            Screen object that handles command-line IO.
        stats : Stats
            Stats object that tracks user statistics.
        """
        self.snippets = snippets
        self.screen = None
        self.stats = stats
        self.current_stat = None
        self.current_position = [0, 0]
        self.state = 0

    def __enter__(self):
        self.screen = Screen()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == KeyboardInterrupt:
            self.stats.save(Config.STATS_PATH)
            return True
        self.screen.deinit()

    def run(self):
        """Main loop logic for typing game."""
        while True:
            self.screen.render(self)
            key = self.screen.get_key()
            self.state = self.get_state(key)

            # # only do rendering stuff here
            if self.state == 0:
                # resize screen
                self.screen.resize()
            if self.state == 1:
                # user is browsing
                # must exit using ctrl + c
                self.browsing(key)
            if self.state == 2:
                # reading user input
                self.typing(key)
            elif self.state == 3:
                # show stats for this snippet
                self.done(key)
            elif self.state == -1:
                # throw keyboard error which exits
                self.save_game()
                raise KeyboardInterrupt
            else:
                raise Exception("wtf")

    def get_state(self, key):
        """Get the state of the game.

        This should return one of the following values:
            0 if the user is in browse mode
            1 if the user is currently typing (ie attempting a code snippet)
            2 if the user had completed a code snippet (similar to browse mode)
            3 if the user is resizing the window
            -1 if the user is attempting to exit the game

        Parameters
        ----------
        key : str or int
            Most recent key pressed by the user.

        Returns
        -------
        int
            Current state of the game.
        """
        keys = {Screen.KEY_BACKSPACE, Screen.KEY_ESCAPE}

        if key == Screen.KEY_RESIZE:
            return 0
        elif self.current_stat is None:
            if key == Screen.KEY_LEFT or key == Screen.KEY_RIGHT:  # TODO spacebar
                return 1
            elif key not in keys:
                # start a new game
                self.start_snippet()
                return 2
        elif (
            self.current_stat.start_time() is not None
            and self.current_stat.end_time() is None
        ):
            return 2
        elif (
            self.current_stat.start_time() is not None
            and self.current_stat.end_time() is not None
        ):
            return 3
        else:
            return -1  ## Eventually be exit

    def typing(self, key):
        """Handles interaction during the typing (gameplay) state."""
        current_entry = self.snippets.current_entry()
        current_snippet = self.snippets.getItem(current_entry)
        current_line = current_snippet.lines[self.current_position[0]]
        current_char = current_line[self.current_position[1]]

        if key == None:
            pass
        elif key == Screen.KEY_ENTER:  # Go to next line
            self.current_position[0] += 1
        elif key == Screen.KEY_BACKSPACE:  # Go back one character
            self.stats.num_wrong -= 1
            self.current_position[1] -= 1
        elif key == Screen.KEY_ESCAPE:  # Stop typing
            # Figure this out later
            # TODO:
            pass
        else:  # key is a typed key
            # If we made it to the end, abort
            if current_line == len(current_snippet.lines) and current_char == len(
                current_line
            ):  # this might be +1
                self.finished_snippet()

            if key == current_char:
                # Right
                self.stats.num_right += 1

            else:
                # Wrong
                self.stats.num_wrong += 1

            self.current_position[1] += 1

    def start_snippet(self):
        """Start snippet"""
        self.current_stat = Stat()
        self.current_stat.start()

    def finished_snippet(self):
        """Finished Snippet"""
        self.current_stat.stop()
        self.stats.update(self.current_stat)

    def done(self, key):
        """Handles interaction during done state."""
        if key == Screen.KEY_LEFT or key == Screen.KEY_RIGHT:  # TODO spacebar
            self.browsing(key)

    def browsing(self, key):
        """Handles interactio during the browsing state."""
        if key == Screen.KEY_LEFT:
            self.snippets.prev_entry()
        elif key == Screen.KEY_RIGHT:
            self.snippets.next_entry()
        self.reset()

    def save_game(self):
        """Save game"""
        self.stats.save(Config.STATS_PATH)

    def reset(self):
        """Resets stats and browses"""
        self.current_stat = None
