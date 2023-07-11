from pathlib import Path
from random import randint

import lorem


def create_lorem_md_post(paragraphs: int = 5):
    s = ""
    for _ in range(paragraphs):
        s += lorem.paragraph() + "\n\n"
    yaml = (
        "---\n" + "title: " + random_word(3) + "\ndate: " + random_date() + "\n---\n\n"
    )
    return yaml + s


def random_word(n=1):
    with open("/usr/share/dict/words") as f:
        words = f.read()
    words = words.split("\n")
    words = [word for word in words if word == word.lower() and "'" not in word]
    return " ".join([words[randint(0, len(words))].capitalize() for _ in range(n)])


def random_date():
    """
    Return YYYY-MM-DD datestring between 2010-01-01 and 2023-06-30.
    """
    return f"{str(randint(1,12)).zfill(2)}/{str(randint(1,28)).zfill(2)}/20{randint(10,23)}"


def save_post(root, i):
    post = create_lorem_md_post()
    with open(Path(root) / "content" / "posts" / f"{i}.md", "w") as f:
        f.write(post)


def main(root):
    for i in range(100):
        save_post(root, i)
