class Snippets:
    def __init__(self, snippets):
        self.snippets = snippets
        self.index = 0

    @classmethod
    def load(cls, filename):
        pass

    def __len__(self):
        pass

    def __getitem__(self, index):
        pass

    def next_entry(self):
        # self.index += 1
        # self.index = self.index % len(self)
        # return self[self.index]
        pass

    def prev_entry(self):
        # self.index -= 1
        # self.index = self.index % len(self)
        # return self[self.index]
        pass


class Snippet:
    def __init__(self, snippet_id, lines, url, author, language):
        self.snippet_id = snippet_id
        self.lines = lines
        self.url = url
        self.author = author
        self.language = language

    @classmethod
    def from_dict(cls, d):
        pass
