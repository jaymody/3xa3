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
        self._reset_row_col()
        self.state = 0

    def _reset_row_col(self):
        snip = self.snippets.current_snippet()
        self.row = 0
        self.col = len(snip.lines[0]) - len(snip.lines[0].lstrip())

    def __enter__(self):
        self.screen = Screen()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.screen.deinit()
        if exc_type == KeyboardInterrupt:
            self.stats.save(Config.STATS_PATH)
            return True  # don't throw KeyboardInterrupt

    def run(self):
        """Main loop logic for typing game."""
        self.screen.render_snippet(self)

        while True:
            key = self.screen.get_key()
            self.state = self.get_state(key)

            # only do rendering stuff here
            if self.state == 0:
                # resize screen
                self.screen.resize(self)
            elif self.state == 1:
                # user is browsing
                # must exit using ctrl + c
                self.browsing(key)
            elif self.state == 2:
                # reading user input
                self.typing(key)
            elif self.state == 3:
                # show stats for this snippet
                self.done(key)
            elif self.state == -1:
                # throw keyboard error which exits
                raise KeyboardInterrupt
            else:
                raise KeyboardInterrupt

    def get_state(self, key):
        """Get the state of the game.

        This should return one of the following values:
            0 if the user is resizing the window
            1 if the user is in browse mode
            2 if the user is currently typing (ie attempting a code snippet)
            3 if the user had completed a code snippet (similar to browse mode)
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
        if key == Screen.KEY_RESIZE:
            return 0
        elif self.current_stat is None:
            keys = {Screen.KEY_LEFT, Screen.KEY_RIGHT, None}
            if key in keys:
                return 1
            elif key == Screen.KEY_ESCAPE:
                return -1
            else:
                # start a new game
                self.start_snippet()
                return 2
        elif (
            self.current_stat.start_time is not None
            and self.current_stat.end_time is None
        ):
            return 2
        elif (
            self.current_stat.start_time is not None
            and self.current_stat.end_time is not None
        ):
            return 3
        else:
            return -1

    def typing(self, key):
        """Handles interaction during the typing (gameplay) state.

        This handling of interaction includes special characters (Enter,
        backspace, escape) as well as normal keystrokes (letters, numbers,
        special characters).

        Parameters
        ----------
        key: str or int
            Most recent key pressed by the user.
        """

        current_snippet = self.snippets.current_snippet()
        current_line = current_snippet.lines[self.row]
        current_char = None

        def calculate_whitespace(row):
            """Calculates whitespace between the beginning of the line and when
            the text starts. Used for correctly rendering cursor location."""
            return len(current_snippet.lines[row]) - len(
                current_snippet.lines[row].lstrip()
            )

        def end_of_line():
            """Deduces whether the cursor has made it to the end of the currently
            typed line.

            Returns
            -------
            bool
                Whether the user is at the end of the line or not."""
            return (
                self.col == len(current_line)
                and self.row != len(current_snippet.lines) - 1
            )

        def end_of_snippet():
            """Deduces whether the cursor has made it to the end of the currently
            typed snippet.

            Returns
            -------
            bool
                Whether the user is at the end of the snippet or not.
            """
            return (
                self.col == len(current_line)
                and self.row == len(current_snippet.lines) - 1
            )

        if not end_of_line():
            current_char = current_line[self.col]

        action = None

        if key == None:
            pass
        elif key == Screen.KEY_ENTER:  # Go to next line
            if end_of_line():
                self.row += 1
                self.current_stat.num_lines += 1
                while current_snippet.lines[self.row] == "":
                    self.row += 1
                self.col = calculate_whitespace(self.row)
                action = "enter"
        elif key == Screen.KEY_BACKSPACE:  # Go back one character
            if self.row == 0 and calculate_whitespace(self.row) == self.col:
                # First character of first line -> pass
                return
            # self.current_stat.num_wrong -= 1
            if calculate_whitespace(self.row) == self.col:
                # 0th char of a row -> up 1 row, last col
                self.row -= 1
                self.col = len(current_snippet.lines[self.row]) - 1
            else:
                #'normal' backspace
                self.col -= 1
            action = "back"
        elif key == Screen.KEY_ESCAPE:  # Stop typing
            self.reset_snippet()
            return
        else:  # key is a typed key
            if current_char == None:
                pass
            elif key == current_char:
                # Right
                self.current_stat.num_correct += 1
                action = "correct"
                self.col += 1
                self.current_stat.num_chars += 1
            else:
                # Wrong
                self.current_stat.num_wrong += 1
                action = "incorrect"
                self.col += 1
                self.current_stat.num_chars += 1

        self.screen.render_update(self, action)

        # If we made it to the end, call done game
        if end_of_snippet():
            self.current_stat.num_lines += 1
            self.finished_snippet()

    def start_snippet(self):
        """Start snippet"""
        self._reset_row_col()
        self.current_stat = Stat()
        self.current_stat.start()

    def finished_snippet(self):
        """Finished Snippet"""
        self.current_stat.stop()
        self.stats.update(self.current_stat)
        self.screen.render_score(self)

    def done(self, key):
        """Handles interaction during done state.

        Parameters
        ----------
        key: str or int
            Most recent key pressed by the user.
        """
        if key == Screen.KEY_LEFT or key == Screen.KEY_RIGHT:
            self.browsing(key)
        elif key == Screen.KEY_ESCAPE:
            raise KeyboardInterrupt
        elif key not in {None, Screen.KEY_ENTER, Screen.KEY_BACKSPACE}:
            self.reset_snippet()
            self.start_snippet()
            self.typing(key)

    def browsing(self, key):
        """Handles interaction during the browsing state.

        Parameters
        ----------
        key: str or int
            Most recent key pressed by the user.
        """
        if key == Screen.KEY_LEFT:
            self.snippets.prev_snippet()
            self.reset_snippet()
        elif key == Screen.KEY_RIGHT:
            self.snippets.next_snippet()
            self.reset_snippet()
        elif key == Screen.KEY_ESCAPE:
            raise KeyboardInterrupt

    def reset_snippet(self):
        """Resets stats and browses"""
        self._reset_row_col()
        self.current_stat = None
        self.screen.render_snippet(self)
