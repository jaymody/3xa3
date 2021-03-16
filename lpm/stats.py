def lines_per_minute(num_lines, elapsed):
    pass


def words_per_minute(num_chars, elapsed):
    """just fake words per minute based on average number of chars in a word."""
    # 5.6
    pass


def characters_per_minute(num_chars, elapsed):
    pass


def accuracy(correct, wrong):
    pass


class Stats:
    def __init__(self, data):
        # self.stats = {
        #     "session timestamp": (wpm, lpm, cpm, accuracy),
        #     "session timestamp": (wpm, lpm, cpm, accuracy),
        #     "session timestamp": (wpm, lpm, cpm, accuracy),
        #     "session timestamp": (wpm, lpm, cpm, accuracy),
        # }
        # self.current_stats = [(wpm, lpm, cpm, accuracy), (wpm, lpm, cpm, accuracy)]
        pass

    def update(self, num_chars, num_lines, elapsed):
        """For a singular snippet."""
        pass

    @classmethod
    def load(cls, filename):
        pass

    def save(self, filename):
        pass
