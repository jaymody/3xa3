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
    def __init__(self, num_lines=0, num_chars=0, num_correct=0, num_wrong=0, elapsed=0):
        """Stats for a single snippet.

        Parameters
        ----------
        num_lines : int, optional
            [description], by default 0
        num_chars : int, optional
            [description], by default 0
        num_correct : int, optional
            [description], by default 0
        num_wrong : int, optional
            [description], by default 0
        elapsed : int, optional
            [description], by default 0
        """
        self.num_lines = num_lines
        self.num_chars = num_chars
        self.num_correct = num_correct
        self.num_wrong = num_wrong
        self.elapsed = elapsed


class Stats:
    def __init__(self, stats, current=None):
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
        """[summary]

        Parameters
        ----------
        filename : [type]
            [description]
        """
        pass

    def save(self, filename):
        """[summary]

        Parameters
        ----------
        filename : [type]
            [description]
        """
        pass
