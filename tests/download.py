import requests
from lpm.snippets import Snippet, Snippets

if __name__ == "__main__":
    with open("tests/urls.txt") as fi:
        urls = fi.readlines()

    snippets = []
    for i, url in enumerate(urls):
        # TODO: add try except if something goes wrong for a given url
        # get author (ie jaymody/linkipedia)
        author = url.split("/blob/")[0].split("github.com/")[-1]

        # get line numbers
        l1, l2 = [int(n[1:]) for n in url.split("#")[-1].split("-")]

        # get code
        raw_url = url.replace("/blob/", "/raw/", 1)
        code = requests.get(raw_url).text
        code = code.splitlines()
        code = code[l1 - 1 : l2]
        code = [line.rstrip() for line in code]

        # get language
        ext_to_lang = {"java": "java", "py": "python", "js": "javascript"}
        ext = url.split("#")[-2].split(".")[-1]
        lang = ext_to_lang[ext]

        print(f"\n\n\n\n--- {author}, {lang} ---")
        print("\n".join(code))

        snippets.append(Snippet(i, code, url, author, lang))

    snippets = Snippets(snippets)
    snippets.save("tests/data/snippets.pickle")
