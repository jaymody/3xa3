"""Module that specifies data structures, namely Snippet and Snippets."""


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
        pass


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

    @classmethod
    def load(cls, filename, languages):
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
        # set(languages)
        # snippets = []
        # for k, values in json.items():
        #     if k in languages:
        #         snippets += [v.from_dict(v) v in values]
        # return cls(snippets)
        pass

    def __len__(self):
        """Returns number of snippets."""
        pass

    def __getitem__(self, index):
        """Loads the code snippet corresponding to the requested index.

        Parameters
        ----------
        index : int
            Index of the requested code snippet.
        """
        pass

    def shuffle(self):
        """Shuffle the list of snippets."""
        pass

    def next_entry(self):
        """Returns the next entry in the list of code snippets."""
        # self.index += 1
        # self.index = self.index % len(self)
        # return self[self.index]
        pass

    def prev_entry(self):
        """Returns the previous entry in the list of code snippets."""
        # self.index -= 1
        # self.index = self.index % len(self)
        # return self[self.index]
        pass


# {
#     "python": [
#         {
#             "snippet_id": 0,
#             "lines": ["print('hello')", "print('hi')"],
#             "url": "github.com",
#             "author": "jay",
#             "language": "python",
#         },
#         {
#             "snippet_id": 0,
#             "lines": ["print('hello')", "print('hi')"],
#             "url": "github.com",
#             "author": "jay",
#             "language": "python",
#         },
#     ],
#     "java": [
#         {
#             "snippet_id": 0,
#             "lines": ["print('hello')", "print('hi')"],
#             "url": "github.com",
#             "author": "jay",
#             "language": "python",
#         },
#         {
#             "snippet_id": 0,
#             "lines": ["print('hello')", "print('hi')"],
#             "url": "github.com",
#             "author": "jay",
#             "language": "python",
#         },
#     ],
# }
