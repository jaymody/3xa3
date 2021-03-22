"""Module that specifies data structures, namely Snippet and Snippets."""
import random
import pickle

from .config import Config


class Snippet:
    def __init__(self, snippet_id, lines, url, author, language):
        """Data for a single code snippet.

        Parameters
        ----------
        snippet_id : int
            Unique ID for each code snippet.
        lines : list[str]
            Text lines in the code snippet.
        url : str
            A link to the source of the code snippet (ie full url to github
            source file with lines permalinked)
        author : str
            The author of the code snippet (ie pallets/flask).
        language : str
            The programming language in which the code snippet is written.
        """
        self.snippet_id = snippet_id
        self.lines = lines
        self.url = url
        self.author = author
        self.language = language


class Snippets:
    def __init__(self, snippets):
        """Stores database of code snippets.

        Parameters
        ----------
        snippets : list[Snippet]
            A list of Snippet objects.
        """
        self.snippets = snippets
        self.index = 0
        self.shuffle()

    def __len__(self):
        """Returns number of snippets."""
        return len(self.snippets)

    def __iter__(self):
        for s in self.snippets:
            yield s

    def shuffle(self):
        """Shuffle the list of snippets."""
        random.shuffle(self.snippets)

    def current_snippet(self):
        """Get current entry"""
        return self.snippets[self.index]

    def next_snippet(self):
        """Returns the next entry in the list of code snippets."""
        self.index += 1
        self.index = self.index % len(self)
        return self.snippets[self.index]

    def prev_snippet(self):
        """Returns the previous entry in the list of code snippets."""
        self.index -= 1
        self.index = self.index % len(self)
        return self.snippets[self.index]

    @staticmethod
    def load(filename, languages=Config.DEFAULT_LANGS):
        """Loads snippets from specified filename.

        Parameters
        ----------
        filename : str
            A direct path to the filename to load snippets from.

        languages : list[str]
            List of string of languages to load snippets of.

        Returns
        -------
        Snippets
            Returns Snippets object loaded from filename.
        """
        languages = set(languages)

        with open(filename, "rb") as fi:
            snippets = pickle.load(fi)

        snippets.snippets = [s for s in snippets.snippets if s.language in languages]
        snippets.shuffle()
        return snippets

    def save(self, filename):
        """Saves current statistics to the specified pickle file.

        Parameters
        ----------
        filename : str
            File path to save stats to.
        """
        with open(filename, "wb") as fo:
            pickle.dump(self, fo)
