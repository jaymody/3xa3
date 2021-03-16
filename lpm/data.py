class Snippets:
    def __init__(self, snippets):
        """[summary]

        Parameters
        ----------
        snippets : [type]
            [description]
        """
        self.snippets = snippets
        self.index = 0

    @classmethod
    def load(cls, filename):
        """[summary]

        Parameters
        ----------
        filename : [type]
            [description]
        """
        pass

    def __len__(self):
        """[summary]"""
        pass

    def __getitem__(self, index):
        """[summary]

        Parameters
        ----------
        index : [type]
            [description]
        """
        pass

    def next_entry(self):
        """[summary]"""
        # self.index += 1
        # self.index = self.index % len(self)
        # return self[self.index]
        pass

    def prev_entry(self):
        """[summary]"""
        # self.index -= 1
        # self.index = self.index % len(self)
        # return self[self.index]
        pass


class Snippet:
    def __init__(self, snippet_id, lines, url, author, language):
        """[summary]

        Parameters
        ----------
        snippet_id : [type]
            [description]
        lines : [type]
            [description]
        url : [type]
            [description]
        author : [type]
            [description]
        language : [type]
            [description]
        """
        self.snippet_id = snippet_id
        self.lines = lines
        self.url = url
        self.author = author
        self.language = language

    @classmethod
    def from_dict(cls, d):
        """[summary]

        Parameters
        ----------
        d : [type]
            [description]
        """
        pass
