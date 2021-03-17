class Game:
    def __init__(self, config, snippets, screen, stats):
        """[summary]

        Parameters
        ----------
        config : [type]
            [description]
        snippets : [type]
            [description]
        screen : [type]
            [description]
        stats : [type]
            [description]
        """
        self.config = config
        self.snippets = snippets
        self.screen = screen
        self.stats = stats
        self.state = 0

    def run(self):
        """Main method for the game. Handles logic for user input."""
        # state = 0 for browsing, 1 for typing, 2 for done, 3 for resize, -1 for quit
        while True:
            self.screen.render(self)
            key = self.screen.get_key()
            state = self.handle_state(key)

            # # only do rendering stuff here
            # if state == 0:
            #     # reading user input
            #     self.typing()
            # elif state == 1:
            #     # show stats for this snippet
            #     self.done()
            # elif state == 2:
            #     # user is browsing
            #     # must exit using ctrl + c
            #     self.browsing()
            # elif state == 3:
            #     # resize screen
            #     self.screen.resize()
            # elif state == -1:
            #     # throw keyboard error which exits
            #     pass
            # else:
            #     # panic??????!!!
            #     pass

    def handle_state(self, key):
        """[summary]

        Parameters
        ----------
        key : [type]
            [description]
        """
        pass

    def typing(self):
        """Handles interaction while user is typing characters in gameplay."""
        pass

    def done(self):
        """Handles the user having finished playing lpm"""
        pass

    def browsing(self):
        """Handles user browsing through multiple code snippets."""
        pass
