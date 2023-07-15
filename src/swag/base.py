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
        self.meta = {}

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
            title = ''
        if 'date' in self.meta.keys():
            date = f"<p>{pd.Timestamp(self.meta['date']).date()}</p>"
        else:
            date = ''
        body = title + date + self.content
        self.html = self.template.replace("{{ body }}", body)

    def write(self, filename=None):
        name = None
        if filename is None:
            name = self._content.name.replace('.md','.html') 
            filename = self._content.parent / name
        print(f'_content: {self._content}; name: {name}; filename: {filename}'
              )
        self.href = filename
        with open(self._root / 'build' / filename, 'w') as f:
                  f.write(self.html)

    def get_summary(self):
        name = self._content.name.replace('.md',
                                                                 '.html')
        title = f'<h1><a href="{name}">{self.meta["title"]}</a></h1>'
        date = f'<p>{self.meta["date"]}</p>'
        return f'<div>{title}{date}</div>'


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
                page = Page(content = fpath)
                page.load_template()
                page.load_raw_content()
                page.convert_raw_content()
                page.make_page()
                page.write()
                summaries.append(page.get_summary())

            else:
                os.mkdir(self.root / 'build' / fpath)
                subfolder_summary = self._build_content(fpath)
                summaries.append(subfolder_summary)
        page = Page(content=basepath)
        page.load_template()
        page.content = ''.join(summaries)
        page.make_page()
        page.write(filename=basepath / 'index.html')
        return f'<div><a href="/{basepath}">{basepath.name.capitalize()} Index</a></div>' 


    def get_template(self, name):
        if name not in self._templates.keys():
            pass # load template
        return self._template[name]

def main():
    builder = Builder()
    builder.restart()
    builder.build()
