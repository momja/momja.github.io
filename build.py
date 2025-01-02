from genericpath import exists
from tokenize import String
from cv2 import Formatter_FMT_CSV
from staticjinja import Site
import frontmatter
import yaml
import markdown2 as md
from pathlib import Path
import glob
import os
import argparse
from pygments import formatters
import datetime
import feedgenerator
import re

import projectJSONParser

build_path = "./static"
html_article_dir = "articles/"
articles_metadata = []
articles_data = {}

image_link_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

context = {}

def replace_img_src(m):
    # Replace all occurrences of '../' in img path unless it's a full URL
    if (m.group(2).startswith("https://") or context['dev']):
        # We keep relative links on development
        return '![{}]({})'.format(m.group(1), m.group(2))
    img_path = re.sub(r'\.\.\/', '', m.group(2))
    if img_path.endswith('.png'):
        img_path = img_path[:-4] + '.jpg'
    print(img_path)
    base_url = 'http://dizzard.net/'

    return '![{}]({})'.format(m.group(1), os.path.join(base_url, img_path))


markdowner = md.Markdown(
    extras={
        'fenced-code-blocks': None,
        'html-classes': {
            'code': 'codeblock',
            'pre': 'codewrapper',
            'ol': 'list-decimal'},
        'cuddled-lists': None},
    safe_mode=False)

def md_context_for_template(template):
    """
    Generates Markdown context for a given template.

    Parameters:
        template (jinja2.Template): A template object.

    Returns:
        dict: Markdown context.
    """
    return md_context(template.filename)


def md_context(filename, include_content=True):
    """
    Generates Markdown context from a file with metadata.

    Parameters:
        filename (str): Name of the file.
        include_content (bool, optional): Boolean value indicating whether content should be included (default: True).

    Returns:
        dict: Article data with metadata.
    """
    metadata_file = os.path.splitext(filename)[0] + ".yml"
    article_data = {}
    if not exists(metadata_file):
        # Use frontmatter if there isn't a yaml file
        post = frontmatter.load(filename)
        if not post.metadata:
            raise Exception(f"metadata is not present in a YAML file or as frontmatter for {filename}. Please update.")
        if include_content:
            markdown_content = re.sub(image_link_pattern, replace_img_src, post.content)
            article_data['content'] = markdowner.convert(markdown_content)
        article_data.update(post.metadata)
        return article_data

    markdown_content = Path(filename).read_text()
    if include_content:
        markdown_content = re.sub(image_link_pattern, replace_img_src, markdown_content)
        article_data['content'] = markdowner.convert(markdown_content)
    with open(metadata_file, 'r') as f:
        metadata = yaml.load(f, Loader=yaml.Loader)
        article_data.update(metadata)
    articles_data[article_data["title"]] = article_data
    return article_data


def html_context(template):
    """
    Generates HTML context for a given template file.

    Parameters:
        template (jinja2.Template): A template file.

    Returns:
        dict: Article data with HTML content.
    """
    html_content = Path(template.filename).read_text()
    article_data = {"content": html_content}
    metadata_file = os.path.splitext(template.filename)[0] + ".yml"
    try:
        with open(metadata_file, 'r') as f:
            metadata = yaml.load(f, Loader=yaml.Loader)
            article_data.update(metadata)
    except:
        print(f"Configuration file does not exist for {metadata_file}")
    articles_data[article_data["title"]] = article_data
    return article_data


def article_metadata(template):
    """
    Retrieves metadata for all articles in a directory.

    Parameters:
        template: A template object.

    Returns:
        dict: Metadata for all articles in a sorted manner.
    """
    article_dir = "./src/articles/"
    md_file_dirs = glob.glob(os.path.join(article_dir, "*/"))
    for i, dir in enumerate(md_file_dirs):
        try:
            article_file = glob.glob(os.path.join(dir, '*.md'))
            if not article_file:
                # TODO: Max This is really lazy
                article_file = glob.glob(os.path.join(dir, '*.html'))[0]
            else:
                article_file = article_file[0]
            data = md_context(article_file, True)
            if data["publish_date"]:
                data["date"] = data["publish_date"].strftime('%b %d %Y')
            data["path"] = os.path.join("articles", os.path.basename(os.path.split(dir)[0]), os.path.basename(os.path.splitext(article_file)[0]) + '.html')
            articles_metadata.append(data)
        except:
            print(f"Failed to load article file in {dir}")

    articles_metadata.sort(key=lambda article: article["publish_date"], reverse=True)
    return {"articles": articles_metadata}


def render_md(site: Site, template, **kwargs):
    """
    Renders Markdown content to HTML.

    Parameters:
        site (staticjinja.Site): Site object.
        template (jinja2.Template): Template object.
        **kwargs: Keyword arguments.

    Returns:
        None
    """
    out = site.outpath / Path(template.name).with_suffix(".html")
    os.makedirs(out.parent, exist_ok=True)
    site.get_template("helper_templates/_article.html").stream(**kwargs).dump(str(out), encoding="utf-8")


def generate_rss():
    feed = feedgenerator.Rss201rev2Feed(
        title="Dizzard's RSS Feed",
        link="http://dizzard.net/",
        description="Latest Articles from Max Omdal (dizzard.net)",
        image="images/favicon.png",
    )
    # articles_metadata is sorted by publish date in reverse.
    # We re-reverse it to add the feed items in the correct order
    # Which is essential to have the right index (guid)
    for index, article in enumerate(articles_metadata):
        article_link = f"http://dizzard.net/{article.get('path')}"
        unique_id = len(articles_metadata) - index
        pub_date_str = article.get("publish_date", "").strftime('%a, %d %b %Y %H:%M:%S +0000') \
            if isinstance(article.get("publish_date", ""), datetime.date) \
            else article.get("publish_date", "")

        content = "<![CDATA[{}]]>".format(article.get("content", ""))
        feed.add_item(
            title=article.get("title", "No Title"),
            link=article_link,
            description=content,
            author_name=article.get("author", "Maxwell Omdal"),
            pubdate=datetime.datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S +0000'),
            unique_id=str(unique_id),
        )

    feed_path = "rss.xml"
    with open(feed_path, 'w') as f:
        feed.write(f, 'utf-8')
        print(f"RSS feed generated and saved to {feed_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build Site')
    parser.add_argument('--full', dest='full', default=False, action='store_true')
    parser.add_argument('--dev', dest='dev', default=False, action='store_true')

    args = parser.parse_args()

    context['dev'] = args.dev

    # build jinja templates
    project_data = projectJSONParser.parse('projects.json')

    # print(list(zip(html_article_files, articles_data)))

    # add pygments css for code highlighting
    code_style = formatters.HtmlFormatter(style='dracula').get_style_defs('.codehilite')
    try:
        os.mkdir(build_path)
    except OSError as error:
        print(error)
    with open(os.path.join(build_path, 'codestyle.css'), 'w+') as css_file:
        css_file.write(code_style)

    site = Site.make_site(searchpath='src',
                          env_globals={'projects':project_data},
                          outpath=build_path,
                          contexts=[(r"articles/.*\.md", md_context_for_template), (r"articles/.*\.html", html_context), ('index.html', article_metadata)],
                          rules=[(r"articles/.*\.md", render_md), (r"articles/.*\.html", render_md)])
    site.render()

    generate_rss()
