class Screen:
    # ESCAPE_KEY
    # BACKSPACE_KEY
    # ENTER_KEY
    # LEFT_KEY
    # RIGHT_KEY
    # RESIZE_KEY

    def __init__(self, something):
        """Initializes typing screen for user 

        Parameters
        ----------
        something : [type]
            [description]
        """
        self.something = something

    def get_key(self):
        """Gets the most recently pressed key

        Returns
        -------
        str | int
            Returns the integer value for a special key, otherwise str value.
        """
        pass

    def resize(self):
        """Resizes game interface based on current user terminal size."""
        pass

    def render(self, game):
        """Renders the header and snippet such that the user can play the game.

        Parameters
        ----------
        game : Game
            The game object is used to render the relevant snippet, statistics,
            and user state.
        """
        pass

    def update_snippet(self):
        """Updates the snippet if the user chooses to view another snippet."""
        pass
