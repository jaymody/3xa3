"""Module for command-line IO."""


class Screen:
    # ESCAPE_KEY
    # BACKSPACE_KEY
    # ENTER_KEY
    # LEFT_KEY
    # RIGHT_KEY
    # RESIZE_KEY

    def __init__(self):
        """Screen object used for command-line IO."""

        # set colors from config
        # initialize curses screen stuff
        pass

    def get_key(self):
        """Gets the most recently pressed key.

        Returns
        -------
        str or int
            Returns the integer value for a special key, otherwise str value.
        """
        pass

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
