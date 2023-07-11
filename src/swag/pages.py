import os
from pathlib import Path

import markdown
import pandas as pd

import swag.build as build


class Post:
    def __init__(self, filename, root):
        self.filename = filename
        self.root = root
        self.s = build.get_post_markdown(self.filename, self.root)
        self.md = markdown.Markdown(extensions=["full_yaml_metadata"])
        self.html = self.md.convert(self.s)
        self.title = self.md.Meta["title"]
        self.name = "".join(
            [
                char
                for char in self.title.lower().replace(" ", "_")
                if char.isalpha() or char == "_"
            ]
        )
        self.date = pd.Timestamp(self.md.Meta["date"])
        self.first_sentence = self.html.replace("<p>", "").split(". ")[0]

    def __repr__(self):
        s = f"Post({self.name})\n"
        s += f"{self.title} {pd.Timestamp(self.date)}\n"
        s += self.first_sentence
        return s

    def make_page(self, root):
        template = build.get_template("minimal", self.root)
        body = f"<h1>{self.title}</h1>" + f"<p>{self.date.date()}</p>" + self.html
        html = template.replace("{{ body }}", body)
        build.write_to_build(root, html, self.name)

    def get_summary(self):
        return f"<a href='{self.name}.html'>{self.title}</a>. ({self.date.day} {self.date.date().strftime('%B')} {self.date.year})"


def get_post_list(root):
    return os.listdir(root / "content" / "posts")
    # return os.listdir(Path(os.getcwd()).parents[0] / 'content' / 'posts')


def get_posts(root):
    return [Post(filename.replace(".md", ""), root) for filename in get_post_list(root)]


def sorted_posts(root):
    return reversed(sorted(get_posts(root), key=lambda x: pd.Timestamp(x.date)))


def make_blog_index(root, posts_per_page=12):
    posts = list(sorted_posts(root))
    template = build.get_template("minimal", root)
    num_index_pages = len(posts) // posts_per_page
    if len(posts) % posts_per_page > 0:
        num_index_pages += 1
    other_pages = "".join(
        [
            f"<a href='{str(k+1).zfill(2)}.html'> {k+1} </a>"
            for k in range(num_index_pages)
        ]
    )
    for i in range(num_index_pages):
        post_list = "".join(
            [
                f"\n<p>{post.get_summary()}</p>\n"
                for post in posts[i * posts_per_page : (i + 1) * posts_per_page]
            ]
        )
        html = template.replace("{{ body }}", post_list)
        s = ""
        if i != 0:
            s += f'<a href=" {str(i).zfill(2)}.html"> << Previous << </a> '
        s += f"| Page {i+1} / {num_index_pages} |"
        if i + 1 < num_index_pages:
            s += f'<a href=" {str(i+2).zfill(2)}.html">  >> Next >> </a> '

        html = html + f'<div align="center"><p>{s}</p><p>{other_pages}</p></div>'

        build.write_to_build(root, html, str(i + 1).zfill(2))


def make_home():
    template = build.get_template("minimal")
    html = template.replace("{{ body }}", "<img src='assets/pprescott_avatar.jpeg'>")
    build.write_to_build(html, "index")


def main(root):
    # make_home()
    make_blog_index(root)
    [p.make_page(root) for p in sorted_posts(root)]


if __name__ == "__main__":
    main()
