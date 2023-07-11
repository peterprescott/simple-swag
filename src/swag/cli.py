import os
from pathlib import Path

import fire

import swag


def hello(name="World"):
    return f"Hello {name}!"


def start(here=""):
    root = Path(os.getcwd()) / here
    for folder in ["templates", "content", "assets"]:
        if not os.path.exists(root / folder):
            os.mkdir(root / folder)
    for subfolder in ["posts", "pages"]:
        if not os.path.exists(root / "content" / subfolder):
            os.mkdir(root / "content" / subfolder)
    swag.lorem_posts.main(root)
    swag.build.main(root)


def main():
    fire.Fire()
