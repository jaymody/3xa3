"""Module for tracking and computing lpm statistics."""


def lines_per_minute(num_lines, elapsed):
    """Calculates lines per minute.

    Parameters
    ----------
    num_lines : int
        Number of lines typed during elapsed time.
    elapsed : double
        Number of seconds elapsed in user's typing.

    Returns
    -------
    double
        Number of lines per minute a user is typing.
    """
    pass


def words_per_minute(num_chars, elapsed):
    """Calculates words per minute based on average 5.6 characters per word.

    Parameters
    ----------
    num_chars : int
        Number of characters typed during elapsed time.
    elapsed : double
        Number of seconds elapsed in user's typing.

    Returns
    -------
    double
        Number of words per minute a user is typing.
    """
    pass


def characters_per_minute(num_chars, elapsed):
    """Calculates characters per minute.

    Parameters
    ----------
    num_chars : int
        Number of characters typed during elapsed time.
    elapsed : double
        Number of seconds elapsed in user's typing.

    Returns
    -------
    double
        Number of characters per minute a user is typing.
    """
    pass


def accuracy(correct, wrong):
    """Calculates user accuracy for a given section.

    Parameters
    ----------
    correct : int
        Number of characters correctly typed
    wrong : int
        Number of characters incorrectly typed

    Returns
    -------
    double
        The user's fractional accuracy for the given accuracy
    """
    pass


class Stat:
    def __init__(self, start_time, end_time=None):
        """Statistics for a single snippet attempt.

        Parameters
        ----------
        start_time : datetime
            Datetime object for when attempt was started.
        end_time : datetime, optional
            Datetime object for when attempt was completed.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.num_lines = 0
        self.num_chars = 0
        self.num_correct = 0
        self.num_wrong = 0

    @property
    def elapsed(self):
        """Elapsed time in seconds since stat was started."""
        pass

    @property
    def lpm(self):
        """Lines per minute."""
        pass

    @property
    def wpm(self):
        """Words per minute."""
        pass

    @property
    def cpm(self):
        """Characters per minute."""
        pass

    @property
    def acc(self):
        """Accuracy."""
        pass


class Stats:
    def __init__(self, stats):
        """Data object for user statistics.

        Parameters
        ----------
        stats : dict datetime.datime -> Stat
            A history of user snippet statistics stored in a dictionary that
            maps a datetime to a Stat object.
        """
        self.stats = stats

    def update(self, stat):
        """Update the stats history with a new Stat entry.

        Parameters
        ----------
        stat : Stat
            Stat for the current
        """
        pass

    @classmethod
    def load(cls, filename):
        """Loads stats from the provided stats JSON file.

        Parameters
        ----------
        filename : str
            File path to load stats from.
        """
        pass

    def save(self, filename):
        """Saves current statistics to the specified JSON file.

        Parameters
        ----------
        filename : str
            File path to save stats to.
        """
        pass
