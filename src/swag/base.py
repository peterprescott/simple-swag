import os
from pathlib import Path

import markdown
import pandas as pd

def get_project_root(max_depth=3):
    required = ('assets', 'content', 'templates', 'config.toml')
    found = False
    position = Path(os.getcwd())
    depth = 0

    while not found:
        if depth == max_depth:
            print('swag could not find project root')
            return None

        ls = os.listdir(position)
        if sum([r in ls for r in required]) / len(required) >= 1/2:
            root = position
            found = True
        else:
            depth +=1
            try:
                position = position.parents[0]
            except IndexError:
                print(f'{position} has no parents')
                depth = max_depth

    return root

class Page:
    def __init__(self, template='minimal', content=None,):
        self._template = template
        self._content = content
        self._root = Path(get_project_root())
        self._md_interpreter = markdown.Markdown(
                extensions=["full_yaml_metadata"])

    def load_template(self, template):
        with open(self._root / 'templates' / f'{self._template}.html') as f:
            self.template = f.read()

    def load_raw_content():
        with open(self._root / 'content' / self._content) as f:
            self.raw_content = f.read()

    def convert_raw_content():
        if '.md' in self._content:
            self.content = self._md_interpreter.convert(self.raw_content)
            self.meta = self._md_interpreter.Meta.copy()
        else:
            self.content = self.raw_content
            self.meta = {}

    def make_page():
        pass




page = Page()

