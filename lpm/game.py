"""Module that contains main logic for lpm typing game."""


class Game:
    def __init__(self, snippets, screen, stats):
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
        self.screen = screen
        self.stats = stats
        self.current_stat = None
        self.state = 0

    def run(self):
        """Main loop logic for typing game."""
        while True:
            self.screen.render(self)
            key = self.screen.get_key()
            self.state = self.get_state(key)

            # # only do rendering stuff here
            # if state == 0:
            #     # user is browsing
            #     # must exit using ctrl + c
            #     self.browsing()
            # if state == 1:
            #     # reading user input
            #     self.typing()
            # elif state == 2:
            #     # show stats for this snippet
            #     self.done()
            # elif state == 3:
            #     # resize screen
            #     self.screen.resize()
            # elif state == -1:
            #     # throw keyboard error which exits
            #     pass
            # else:
            #     # panic??????!!!
            #     pass

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
        pass

    def typing(self):
        """Handles interaction during the typing (gameplay) state."""
        pass

    def done(self):
        """Handles interaction during done state."""
        pass

    def browsing(self):
        """Handles interactio during the browsing state."""
        pass
