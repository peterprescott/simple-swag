import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import shutil

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

    start_folder_path = Path(__file__).parents[1] / 'start'
    for f in os.listdir(start_folder_path):
        if '.html' in f:
            shutil.copyfile(src=start_folder_path / f, dst=root /
                            'templates' / f)
        else:
            shutil.copyfile(src=start_folder_path / f, dst=root /
                            'assets' / f)

    swag.lorem_posts.main(root)
    swag.build.main(root)

def serve():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(directory='build', *args, **kwargs)
    server = HTTPServer(("localhost", 8000), Handler)
    server.serve_forever()



def main():
    fire.Fire()
