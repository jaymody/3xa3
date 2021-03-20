"""Module that specifies data structures, namely Snippet and Snippets."""
import json
import random

DEFAULT = ["python", "java", "javascript"]


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

    @classmethod
    def from_dict(cls, d):
        """Build Snippet object from a dictionary.

        Parameters
        ----------
        d : dict
            Dictionary containing snippet data.
        """
        return Snippet(
            d["snippet_id"], d["lines"], d["url"], d["author"], d["language"]
        )


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

    def __len__(self):
        """Returns number of snippets."""
        return len(self.snippets)

    def __getitem__(self, index):
        """Loads the code snippet corresponding to the requested index.

        Parameters
        ----------
        index : int
            Index of the requested code snippet.
        """
        try:
            return self.snippets[index]
        except IndexError:
            return None

    def shuffle(self):
        """Shuffle the list of snippets."""
        random.shuffle(self.snippets)

    def next_entry(self):
        """Returns the next entry in the list of code snippets."""
        self.index += 1
        self.index = self.index % len(self)
        return self[self.index]

    def prev_entry(self):
        """Returns the previous entry in the list of code snippets."""
        self.index -= 1
        self.index = self.index % len(self)
        return self[self.index]

    @classmethod
    def load(cls, filename, languages=DEFAULT):
        """Loads snippets from specified filename

        Parameters
        ----------
        filename : str
            A direct path to the filename to load snippets from. snippets.json
            by default.

        Returns
        -------
        Snippets
            Returns Snippets object loaded from filename.
        """
        with open(filename) as fi:
            data = json.load(fi)
        snippets = []
        for lang, values in data.items():
            if lang in languages:
                snippets += values
        return cls(snippets)
