"""Module for command-line IO."""
import os
import sys
import curses
import locale


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
        min_lines = 12  # min number of lines in terminal required for screen to work
        min_cols = 20  # min number of columns in terminal required for screen to work

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

        # TODO: this is not very good, we should deal with this some other way
        self.cheight = 0
        self.first_key = True
        self.quote = ""
        self.quote_author = ""
        self.quote_columns = 0
        self.quote_coords = tuple()
        self.quote_height = 0
        self.quote_id = 0
        self.quote_lengths = tuple()
        self.quote_title = ""

        # check that terminal is sufficiently large
        # TODO: add this to config? maybe we shouldn't let resize even do this?
        if self.lines < min_lines:
            curses.endwin()
            raise IOError("wpm requires at least %d lines in your display" % min_lines)
        if self.columns < min_cols:
            curses.endwin()
            raise IOError("wpm requires at least %d columns in your display" % min_cols)

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
        # will probably need to use a bunch of helper functions to make this
        # function not big and ugly
        pass
