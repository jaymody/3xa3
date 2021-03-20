"""Module for command-line IO."""
import os
import sys
import curses
import locale

from .config import Config
from .stats import Stat


# TODO: move this to config
# tuples represent a (fg, bg) pair
# (text takes on foreground color, and the background of the text is bg)
COLOR_CONF = {
    "xterm256colors": {
        "background": (233, 233),
        "author": (240, 233),
        "correct": (240, 233),
        "incorrect": (197, 52),
        "prompt": (244, 233),
        "quote": (195, 233),
        "score": (230, 197),
        "top_bar": (51, 24),
    },
    "xtermcolors": {
        "background": (curses.COLOR_BLACK, curses.COLOR_BLACK),
        "author": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "correct": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "incorrect": (curses.COLOR_RED, curses.COLOR_BLACK),
        "prompt": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "quote": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "score": (curses.COLOR_YELLOW, curses.COLOR_RED),
        "top_bar": (curses.COLOR_CYAN, curses.COLOR_BLUE),
    },
    "monochromecolors": {
        "background": (curses.COLOR_BLACK, curses.COLOR_BLACK),
        "author": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "correct": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "incorrect": (curses.COLOR_BLACK, curses.COLOR_WHITE),
        "prompt": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "quote": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "score": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "top_bar": (curses.COLOR_WHITE, curses.COLOR_BLACK),
    },
}


class Screen:
    KEY_BACKSPACE = curses.KEY_BACKSPACE
    KEY_LEFT = curses.KEY_LEFT
    KEY_RIGHT = curses.KEY_RIGHT
    KEY_RESIZE = curses.KEY_RESIZE
    KEY_ENTER = curses.KEY_ENTER
    KEY_ESCAPE = curses.ascii.ESC  # not sure if this will work

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
        os.environ.setdefault("ESCDELAY", esc_delay)

        # use the preferred system encoding
        locale.setlocale(locale.LC_ALL, "")
        self.encoding = locale.getpreferredencoding().lower()

        # initialize curses screen
        self.screen = curses.initscr()
        self.screen.nodelay(True)  # makes getch a non-blocking call
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

        # check that terminal is sufficiently large
        # TODO: add this to config? maybe we shouldn't let resize even do this?
        if self.lines < Config.MAX_LINES:
            curses.endwin()
            raise IOError("lpm requires at least %d lines in your display" % min_lines)
        if self.columns < Config.MAX_COLS:
            curses.endwin()
            raise IOError("lpm requires at least %d columns in your display" % min_cols)

    def setup_colors(self):
        for i, (k, v) in enumerate(COLOR_CONF["xterm256colors"]):
            curses.init_pair(i, *v)
            self.colors[k] = curses.color_pair(i)

        # make certain colors more visible
        if not "xterm256colors":
            self.colors["correct"] |= curses.A_DIM
            self.colors["incorrect"] |= curses.A_UNDERLINE | curses.A_BOLD
            self.colors["quote"] |= curses.A_BOLD
            self.colors["status"] |= curses.A_BOLD

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
            if isinstance(key, int):
                if key == curses.KEY_BACKSPACE:
                    return "KEY_BACKSPACE"
                if key == curses.KEY_LEFT:
                    return "KEY_LEFT"
                if key == curses.KEY_RIGHT:
                    return "KEY_RIGHT"
                if key == curses.KEY_RESIZE:
                    return "KEY_RESIZE"
                return None
            return key
        except curses.error:
            return None

    def _get_key_py27(self):
        """Python 2.7 implementation of get_key."""
        # pylint: disable=too-many-return-statements
        try:
            key = self.window.getkey()

            # Start of UTF-8 multi-byte character?
            if self.encoding == "utf-8" and ord(key[0]) & 0x80:
                multibyte = key[0]
                cont_bytes = ord(key[0]) << 1
                while cont_bytes & 0x80:
                    cont_bytes <<= 1
                    multibyte += self.window.getkey()[0]
                return multibyte.decode(self.encoding)

            if isinstance(key, int):
                if key == curses.KEY_BACKSPACE:
                    return "KEY_BACKSPACE"
                if key == curses.KEY_LEFT:
                    return "KEY_LEFT"
                if key == curses.KEY_RIGHT:
                    return "KEY_RIGHT"
                if key == curses.KEY_RESIZE:
                    return "KEY_RESIZE"
                return None
            return key.decode("ascii")
        except curses.error:
            return None

    @property
    def columns(self):
        """Returns number of terminal columns."""
        return curses.COLS  # pylint: disable=no-member

    @property
    def lines(self):
        """Returns number of terminal lines."""
        return curses.LINES  # pylint: disable=no-member

    def resize(self):
        """Resizes game interface based on current user terminal size."""
        pass

    def render(self, game):
        """Renders the typing interface with the most up to date information.

        Parameters
        ----------
        game : Game
            The game object is used to render the relevant snippet, statistics,
            and user state.
        """
        # render stats
        if game.current_stat:
            self.window.addstr(0, 0, game.current_stat, self.colors["correct"])
        else:
            self.window.addstr(0, 0, Stat(), self.colors["correct"])

        # render author/title
        snip = game.snippets.current_entry()
        self.window.addstr(2, 0, snip.author, self.colors["author"])

        # render lines
        for i, line in enumerate(snip.lines):
            self.window.addstr(4 + i, 0, line, self.colors["prompt"])

        # render final score
        if game.current_stat and game.current_stat.end_time is not None:
            self.window.addstr(
                Config.MAX_LINES + 6, 0, game.current_stat, self.colors["score"]
            )

    # def addstr(self, x_pos, y_pos, text, color=None):
    #     """Wraps call around curses.window.addsr."""
    #     if self.lines > y_pos >= 0:
    #         if x_pos >= 0 and (x_pos + len(text)) < self.columns:
    #             self.window.addstr(y_pos, x_pos, text, color)

    # def chgat(self, x_pos, y_pos, length, color):
    #     """Wraps call around curses.window.chgat."""
    #     if self.lines > y_pos >= 0:
    #         if x_pos >= 0 and (x_pos + length) <= self.columns:
    #             self.window.chgat(y_pos, x_pos, length, color)

    # def set_cursor(self, x_pos, y_pos):
    #     """Sets cursor position."""
    #     if (y_pos < self.lines) and (x_pos < self.columns):
    #         self.window.move(y_pos, x_pos)

    # def right_column(self, y_pos, x_pos, width, text):
    #     """Writes text to screen in columns."""
    #     lengths = self._word_wrap(text, width)

    #     for cur_y, length in enumerate(lengths, y_pos):
    #         self.addstr(
    #             x_pos - length,
    #             cur_y,
    #             text[:length].encode(self.encoding),
    #             self.colors["author"],
    #         )
    #         text = text[1 + length :]

    #     return len(lengths)

    # def update_quote(self, color):
    #     """Renders complete quote on screen."""
    #     quote = self.quote[:]
    #     for y_pos, length in enumerate(self.quote_lengths, 2):
    #         self.addstr(0, y_pos, quote[:length].encode(self.encoding), color)
    #         quote = quote[1 + length :]

    # def update_author(self):
    #     """Renders author on screen."""
    #     author = u"— %s, %s" % (self.quote_author, self.quote_title)
    #     self.cheight = 4 + self.quote_height
    #     self.cheight += self.right_column(
    #         self.cheight - 1, self.quote_columns - 10, self.quote_columns // 2, author
    #     )

    # def update_header(self, text):
    #     """Renders top-bar header."""
    #     self.addstr(0, 0, text, Screen.COLOR_STATUS)
    #     self.chgat(0, 0, self.columns, Screen.COLOR_STATUS)
    #     # self.window.chgat(0, 0, self.columns, Screen.COLOR_STATUS)

    # @staticmethod
    # def _word_wrap(text, width):
    #     """Returns lengths of lines that can be printed without wrapping."""
    #     lengths = []
    #     while len(text) > width:
    #         try:
    #             end = text[: width + 1].rindex(" ")
    #         except ValueError:
    #             break

    #         # We can't divide the input nicely, so just display it as-is
    #         if end == -1:
    #             return [len(text)]

    #         lengths.append(end)
    #         text = text[end + 1 :]

    #     if text:
    #         lengths.append(len(text))

    #     return lengths

    # @staticmethod
    # def _screen_coords(lengths, position):
    #     """Translates quote offset into screen coordinates.

    #     Args:
    #         lengths: List of line lengths for the word-wrapped quote.
    #         position: Offset into the quote that we want to translate to screen
    #                     coordinates.

    #     Returns:
    #         Tuple containing X and Y screen coordinates.
    #     """
    #     y_position = 0

    #     for y_position, line_length in enumerate(lengths):
    #         if position <= line_length:
    #             break
    #         position -= line_length + 1

    #     return position, y_position
