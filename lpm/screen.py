"""Module for command-line IO."""
import os
import sys
import curses
import curses.ascii
import locale

from .config import Config
from .stats import Stat


class Screen:
    KEY_BACKSPACE = curses.KEY_BACKSPACE
    KEY_LEFT = curses.KEY_LEFT
    KEY_RIGHT = curses.KEY_RIGHT
    KEY_RESIZE = curses.KEY_RESIZE
    KEY_ENTER = curses.KEY_ENTER
    KEY_ESCAPE = curses.ascii.ESC

    def __init__(self):
        """Screen object used for command-line IO."""
        # TODO: move this to config?
        esc_delay = 15  # 15ms
        window_timeout = 20  # 20ms

        # min number of lines in terminal required for screen to work
        min_lines = Config.MAX_LINES + 6
        # min number of columns in terminal required for screen to work
        min_cols = Config.MAX_COLS

        # set esc delay to 15 ms
        os.environ.setdefault("ESCDELAY", str(esc_delay))

        # use the preferred system encoding
        locale.setlocale(locale.LC_ALL, "")
        self.encoding = locale.getpreferredencoding().lower()

        # initialize curses screen
        self.screen = curses.initscr()
        self.screen.nodelay(True)  # makes getch a non-blocking call

        # check that terminal is sufficiently large
        # TODO: add this to config? maybe we shouldn't let resize even do this?
        if self.lines < min_lines:
            curses.endwin()
            raise IOError("lpm requires at least %d lines in your display" % min_lines)
        if self.columns < min_cols:
            curses.endwin()
            raise IOError("lpm requires at least %d columns in your display" % min_cols)

        # screen configurations
        self.screen.keypad(True)  # makes curses return keys in form curses.KEY_
        curses.noecho()
        curses.cbreak()

        # set up colors
        self.colors = {}
        curses.start_color()
        self.setup_colors()

        # initialize window
        self.window = curses.newwin(self.lines, self.columns, 0, 0)
        self.window.keypad(True)
        self.window.timeout(window_timeout)
        self.window.bkgd(" ", self.colors["background"])

    def setup_colors(self):
        for i, (k, v) in enumerate(Config.COLORS.items()):
            curses.init_pair(i + 1, *v)
            self.colors[k] = curses.color_pair(i + 1)

        # # make certain colors more visible
        # if not "xterm256colors":
        #     self.colors["correct"] |= curses.A_DIM
        #     self.colors["incorrect"] |= curses.A_UNDERLINE | curses.A_BOLD
        #     self.colors["quote"] |= curses.A_BOLD
        #     self.colors["status"] |= curses.A_BOLD

    @staticmethod
    def is_escape(key):
        """Checks for escape key."""
        if isinstance(key, str) and len(key) == 1:
            return ord(key) == curses.ascii.ESC
        return False

    @staticmethod
    def is_enter(key):
        """Checks for backspace key."""
        if key == Screen.KEY_ENTER:
            return True
        if isinstance(key, str) and ord(key) in (
            curses.ascii.CR,
            10,
            13,
        ):  # TODO: don't use int vals
            return True
        return False

    @staticmethod
    def is_backspace(key):
        """Checks for backspace key."""
        if key == Screen.KEY_BACKSPACE:
            return True
        if isinstance(key, str) and ord(key) in (curses.ascii.BS, curses.ascii.DEL):
            return True
        return False

    def get_key(self):
        """Gets the most recently pressed key.

        Returns
        -------
        str or int
            Returns the integer value for a special key, otherwise str value.
        """
        # pylint: disable=method-hidden
        # Install a suitable get_key based on Python version
        if sys.version_info[0:2] >= (3, 3):
            return self._get_key_py33()
        else:
            return self._get_key_py27()

    def _get_key_py33(self):
        """Python 3.3+ implementation of get_key."""
        # pylint: disable=too-many-return-statements
        try:
            # Curses in Python 3.3 handles unicode via get_wch
            key = self.window.get_wch()
            if self.is_backspace(key):
                return Screen.KEY_BACKSPACE
            elif self.is_enter(key):
                return Screen.KEY_ENTER
            elif self.is_escape(key):
                return Screen.KEY_ESCAPE
            elif isinstance(key, int):
                keymap = set(
                    [
                        Screen.KEY_BACKSPACE,
                        Screen.KEY_LEFT,
                        Screen.KEY_RIGHT,
                        Screen.KEY_RESIZE,
                        Screen.KEY_ENTER,
                        Screen.KEY_ESCAPE,
                    ]
                )
                return None if key not in keymap else key
            return key
        except curses.error:
            return None

    def _get_key_py27(self):
        raise NotImplementedError

    #     """Python 2.7 implementation of get_key."""
    #     # pylint: disable=too-many-return-statements
    #     try:
    #         key = self.window.getkey()

    #         # Start of UTF-8 multi-byte character?
    #         if self.encoding == "utf-8" and ord(key[0]) & 0x80:
    #             multibyte = key[0]
    #             cont_bytes = ord(key[0]) << 1
    #             while cont_bytes & 0x80:
    #                 cont_bytes <<= 1
    #                 multibyte += self.window.getkey()[0]
    #             return multibyte.decode(self.encoding)

    #         if isinstance(key, int):
    #             if key == curses.KEY_BACKSPACE:
    #                 return "KEY_BACKSPACE"
    #             if key == curses.KEY_LEFT:
    #                 return "KEY_LEFT"
    #             if key == curses.KEY_RIGHT:
    #                 return "KEY_RIGHT"
    #             if key == curses.KEY_RESIZE:
    #                 return "KEY_RESIZE"
    #             return None
    #         return key.decode("ascii")
    #     except curses.error:
    #         return None

    @property
    def columns(self):
        """Returns number of terminal columns."""
        return curses.COLS  # pylint: disable=no-member

    @property
    def lines(self):
        """Returns number of terminal lines."""
        return curses.LINES  # pylint: disable=no-member

    def _addstr(self, row, col, text, color=None, encode=True):
        """Wraps call around curses.window.addsr."""
        if encode:
            text = text.encode(self.encoding)

        if self.lines > row >= 0:
            if col >= 0 and (col + len(text)) < self.columns:
                self.window.addstr(row, col, text, color)

    def _chgat(self, row, col, length, color):
        """Wraps call around curses.window.chgat."""
        if self.lines > row >= 0:
            if col >= 0 and (col + length) <= self.columns:
                self.window.chgat(row, col, length, color)

    def _set_cursor(self, row, col):
        """Sets cursor position."""
        if (row < self.lines) and (col < self.columns):
            self.window.move(row, col)

    def clear(self):
        self.window.clear()

    def deinit(self):
        """Deinitializes curses."""
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def resize(self, game):
        """Resizes game interface based on current user terminal size."""
        # TODO: resize
        # max_y, max_x = self.screen.window.getmaxyx()
        # self.screen.clear()

        # # Check if we have the resizeterm ncurses extension
        # if hasattr(curses, "resizeterm"):
        #     curses.resizeterm(max_y, max_x)
        #     # An ungetch for KEY_RESIZE will be sent to let others handle it.
        #     # We'll just pop it off again to prevent endless loops.
        #     self.screen.get_key()

        # self.clear()
        # self.render_snippet(game)
        pass

    def _render_stat(self, stat):
        # if stat is none, use an empty Stat object (shows all 0s)
        top_bar = str(stat) if stat else str(Stat())

        # pad with spaces to the right to overwrite chars if the
        # stats string gets shorter
        top_bar = top_bar.ljust(self.columns - 1)

        self._addstr(0, 0, top_bar, self.colors["top_bar"])

    def _render_author(self, snip):
        text = snip.url
        if len(text) > self.columns - 1:
            text = snip.author

        self._addstr(2, 0, text, self.colors["author"])

    def _render_lines(self, snippet):
        for i, line in enumerate(snippet.lines):
            self._addstr(4 + i, 0, line, self.colors["text"])

    def _render_prompt(self, snip, prompt):
        self._addstr(len(snip.lines) + 5, 0, prompt, self.colors["prompt"])

    def render_snippet(self, game):
        """Renders the typing interface with the most up to date information.

        Parameters
        ----------
        game : Game
            The game object is used to render the relevant snippet, statistics,
            and user state.
        """
        # clear screen
        self.clear()

        snip = game.snippets.current_snippet()

        # render stats
        self._render_stat(game.current_stat)

        # render author
        self._render_author(snip)

        # render lines
        self._render_lines(snip)

        # render prompt
        self._render_prompt(
            snip, "press ESC to quit, ARROWS to browse, or start typing!"
        )

        # set cursor (MUST HAPPEN LAST)
        self._set_cursor(game.row + 4, game.col)

        self.window.refresh()

    def render_update(self, game, action, ret=False):
        """Val is the action that happened right before the given cursor position.

        action = one of back, enter, correct, incorrect, or None
        """
        row, col = game.row + 4, game.col

        # render stats
        self._render_stat(game.current_stat)

        # how do we know what's been updated?
        # set cursor
        # cursor at 4, 0
        # note you cannot go back to prev line
        if action == "back":
            self._chgat(row, col, 1, self.colors["text"])
        elif action == "enter":
            pass
        elif action == "correct":
            self._chgat(row, col - 1, 1, self.colors["correct"])
        elif action == "incorrect":
            self._chgat(row, col - 1, 1, self.colors["incorrect"])
        else:
            # do nothing
            pass

        self._render_prompt(game.snippets.current_snippet(), " " * (self.columns - 1))
        self._set_cursor(row, col)
        self.window.refresh()

    def render_score(self, game):
        self._render_stat(game.current_stat)
        prompt = f"You scored {game.current_stat.lpm:.2f} lpm, press ESC to quit, ARROWS to browse, or start typing!"
        self._render_prompt(game.snippets.current_snippet(), prompt)
