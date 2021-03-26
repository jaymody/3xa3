"""Module that specifies data structures, namely Snippet and Snippets."""
import random
import pickle
from urllib.request import urlopen

from .config import Config


class Snippet:
    ext_to_lang = {"java": "java", "py": "python", "js": "javascript"}

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
    def from_url(cls, snippet_id, url):
        """Create Snippet object from github permalink.

        A url must be of form:
        https://github.com/<USERNAME>/<REPO>/blob/<COMMIT_HASH>/path/to/file.ext#L<START>-L<END>

        For example:
        https://github.com/jaymody/linkipedia/blob/09f3ca27e1ad858a6a010d2ef3d0768cbb9dda36/src/main/java/com/linkipedia/Graph.java#L9-L31

        This will extract the code from the given url and create a Snippet
        object from it. The code will be assigned to lines, the url to url, and
        the author to <USERNAME>/<REPO>. Language will be infered from the
        extension of the file, so the file must have an extension.

        Parameters
        ----------
        snippet_id : int
            Unique ID for the code snippet.
        url : str
            Github permalink.

        Returns
        -------
        Snippet
            Snippet object created using github permalink.
        """
        # author
        author = url.split("/blob/")[0].split("github.com/")[-1]

        # get line numbers
        l1, l2 = [int(n[1:]) for n in url.split("#")[-1].split("-")]

        # get code snippet lines
        # TODO: make this more efficient
        raw_url = url.replace("/blob/", "/raw/", 1)
        with urlopen(raw_url) as response:
            text = response.read().decode("utf-8")
        lines = text.splitlines()
        lines = lines[l1 - 1 : l2]
        # TODO: maybes use config tabs to spaces?
        lines = [line.rstrip().replace("\t", " " * 4) for line in lines]

        # if first line contains whitespace, remove that much whitespace from
        # the rest of the lines
        ws = lambda x: len(x) - len(x.lstrip())
        fws = ws(lines[0])
        lines = [line[min(ws(line), fws) :] for line in lines]

        # get language
        ext = url.split("#")[-2].split(".")[-1]
        language = cls.ext_to_lang[ext]

        return cls(snippet_id, lines, url, author, language)


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

    @classmethod
    def from_urls(cls, urls):
        """Creates snippets object from github permalinks.

        See Snippet.from_url() for more information.

        Parameters
        ----------
        urls : list[str]
            List of github permalink urls.

        Returns
        -------
        Snippets
            Snippets object with snippets from urls.
        """
        # TODO: add try except if something goes wrong for a given url
        # get author (ie jaymody/linkipedia)
        snippets = [Snippet.from_url(i, url) for i, url in enumerate(urls)]
        return cls(snippets)
