import os
import shutil
from pathlib import Path

import markdown

import swag.pages as pages


def get_template(name, root) -> str:
    """
    Return specified HTML template from templates folder as string.
    """
    with open(root / "templates" / f"{name}.html") as f:
        return f.read()


def get_post_markdown(filename, root):
    """
    Return specified markdown post from posts folder as string.
    """
    with open(root / "content" / "posts" / f"{filename}.md") as f:
        return f.read()


def write_to_build(root, html, filename):
    """
    Write html to build folder with specifed filename.
    """
    filepath = root / "build" / f"{filename}.html"
    if not os.path.exists(filepath.parents[0]):
        os.mkdir(filepath.parents[0])
    with open(root / "build" / f"{filename}.html", "w") as f:
        f.write(html)


def main(root):
    build_path = root / "build"
    assets_path = build_path / "assets"
    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    for p in build_path, assets_path:
        os.mkdir(p)
    pages.main(root)
    shutil.copytree(root / "assets", assets_path, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
