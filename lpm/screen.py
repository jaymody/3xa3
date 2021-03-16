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
        """[summary]"""
        pass

    def render(self, game):
        """[summary]

        Parameters
        ----------
        game : [type]
            [description]
        """
        pass

    def update_snippet(self):
        """[summary]"""
        pass
