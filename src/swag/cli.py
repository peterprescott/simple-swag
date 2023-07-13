from random import randint
import os
from pathlib import Path

import fire
from multiavatar.multiavatar import multiavatar

import swag
import swag.resources


def hello(name="World"):
    return f"Hello {name}!"


def start(here=""):
    root = Path(os.getcwd()) / here
    folders = ["templates", "content", "assets"]
    for folder in folders:
        if os.path.exists(root / folder):
            raise Exception("Abort! Static site directories already exist.")    
    for folder in folders:
        if not os.path.exists(root / folder):
            os.mkdir(root / folder)
    for subfolder in ["posts", "pages"]:
        if not os.path.exists(root / "content" / subfolder):
            os.mkdir(root / "content" / subfolder)
    with open(root / "templates" / "minimal.html", 'w') as f: 
        f.write(swag.resources.html_template)
    with open(root / "assets" / "styles.css", 'w') as f: 
        f.write(swag.resources.example_css)
    with open(root / "config.toml", "w") as f:
        f.write(swag.resources.example_config)
    with open(root / "assets" / "avatar.svg", "w") as f:
        f.write(multiavatar(str(randint(0, 1e11)), True, None))

    swag.lorem_posts.main(root)
    swag.build.main(root)


def main():
    fire.Fire()
