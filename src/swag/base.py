import os
from pathlib import Path
import tomllib
import shutil
from functools import cached_property

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
        """
        Parameters
        ----------
        ...
        content: Path
            Relative filepath to {project_root} / 'content'
        ...
        """
        self._template = template
        self._content = content
        self._root = Path(get_project_root())
        self._md_interpreter = markdown.Markdown(
                extensions=["full_yaml_metadata"])
        self.load_template()
        self.load_raw_content()
        self.convert_raw_content()
        self.make_page()

    def load_template(self):
        with open(self._root / 'templates' / f'{self._template}.html') as f:
            self.template = f.read()

    def load_raw_content(self):
        if not self._content:
            return None
        with open(self._root / 'content' / self._content) as f:
            self.raw_content = f.read()

    def convert_raw_content(self):
        if '.md' in self._content.name:
            self.content = self._md_interpreter.convert(self.raw_content)
            self.meta = self._md_interpreter.Meta.copy()
        else:
            self.content = self.raw_content
            self.meta = {}

    def make_page(self):
        if 'title' in self.meta.keys():
            title = f"<h1>{self.meta['title']}</h1>" 
        else:
            title = None
        if 'date' in self.meta.keys():
            date = f"<p>{pd.Timestamp(self.meta['date']).date()}</p>"
        else:
            date = None
        body = title + date + self.content
        self.html = self.template.replace("{{ body }}", body)

    def write(self):
        with open(self._root / 'build' /
                  self._content.parent /
                  (self._content.name.replace('.md','.html')), 'w') as f:
                  f.write(self.html)

    def get_summary(self):
        pass


class IndexPage(Page):
    def make_index_list(self):
        pass



class Builder:
    def __init__(self):
        self.root = get_project_root()
        self._templates = {}

    def restart(self):
        build_path = self.root / 'build'
        assets_path = build_path / 'assets'
        if os.path.exists(build_path):
            shutil.rmtree(build_path)
        os.mkdir(build_path)
        shutil.copytree(self.root / 'assets', assets_path)

    @cached_property
    def config(self):
        with open(f'{self.root}/config.toml', 'rb') as f:
            return tomllib.load(f)

    def build(self):
        self._build_content(basepath = Path('.'))

    def _build_content(self, basepath):
        contents = os.listdir(self.root / 'content' / basepath)
        summaries = []
        for f in contents:
            fpath = basepath / f
            if not os.path.isdir(self.root / 'content' / fpath):
                page = Page(
                        content = fpath
                        # .relative_to(Path('content'))                       
                        )
                page.write()
                summaries.append(page.get_summary())

            else:
                os.mkdir(self.root / 'build' / fpath)
                self._build_content(fpath)
                subfolder_summary = None
                summaries.append(subfolder_summary)

    def get_template(self, name):
        if name not in self._templates.keys():
            pass # load template
        return self._template[name]

def main():
    builder = Builder()
    builder.restart()
    builder.build()
    # md_files = os.listdir('content/posts')

    # pages = [Page(content=f'posts/{f}')
    #          for f in md_files]

    # [p.write() for p in pages]
