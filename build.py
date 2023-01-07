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

import projectJSONParser

build_path = "./static"
html_article_dir = "articles/"
markdowner = md.Markdown(
    '',
    extras={
        'fenced-code-blocks': None,
        'html-classes': {
            'code': 'codeblock',
            'pre': 'codewrapper',
            'ol': 'list-decimal'},
        'cuddled-lists': None},
    safe_mode=False)

def md_context_for_template(template):
    return md_context(template.filename)

def md_context(filename, include_content=True):
    metadata_file = os.path.splitext(filename)[0] + ".yml"
    article_data = {}
    if not exists(metadata_file):
        # Use frontmatter if there isn't a yaml file
        post = frontmatter.load(filename)
        if not post.metadata:
            raise Exception(f"metadata is not present in a YAML file or as frontmatter for {filename}. Please update.")
        if include_content:
            article_data['content'] = markdowner.convert(post.content)
        article_data.update(post.metadata)
        return article_data

    markdown_content = Path(filename).read_text()
    if include_content:
        article_data['content'] = markdowner.convert(markdown_content)
    with open(metadata_file, 'r') as f:
        metadata = yaml.load(f, Loader=yaml.Loader)
        article_data.update(metadata)
    print(article_data)
    return article_data

def html_context(template):
    html_content = Path(template.filename).read_text()
    article_data = {"content": html_content}
    metadata_file = os.path.splitext(template.filename)[0] + ".yml"
    try:
        with open(metadata_file, 'r') as f:
            metadata = yaml.load(f, Loader=yaml.Loader)
            article_data.update(metadata)
    except:
        print(f"Configuration file does not exist for {metadata_file}")
    return article_data

def article_metadata(template):
    articles_data = []
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
            data = md_context(article_file, False)
            if data["publish_date"]:
                data["date"] = data["publish_date"].strftime('%b %d %Y')
            data["path"] = os.path.join("articles", os.path.basename(os.path.split(dir)[0]), os.path.basename(os.path.splitext(article_file)[0]) + '.html')
            articles_data.append(data)
        except:
            print(f"Failed to load article file in {dir}")

    articles_data.sort(key=lambda article: article["publish_date"], reverse=True)
    return {"articles": articles_data}

def render_md(site, template, **kwargs):
    out = site.outpath / Path(template.name).with_suffix(".html")
    os.makedirs(out.parent, exist_ok=True)
    site.get_template("helper_templates/_article.html").stream(**kwargs).dump(str(out), encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build Site')
    parser.add_argument('--full', dest='full', default=False, action='store_true')

    args = parser.parse_args()
    # convert md pages to html
    # md_file_dirs = sorted(glob.glob(os.path.join(article_dir, "*/")), key=os.path.getmtime)
    # html_article_files = convertMDToHTML(md_file_dirs, builddir='src', outdir='/articles/', full=args.full)

    # build jinja templates
    project_data = projectJSONParser.parse('projects.json')

    # Pair every html article with its YAML file
    # articles_data = []
    # for i, dir in enumerate(md_file_dirs):
        # try:
            # data_file = glob.glob(os.path.join(dir, '*.yml'))[0]
            # with open(data_file, 'r') as f:
                # data = yaml.load(f, Loader=yaml.Loader)
                # print(data_file)
                # data["path"] = html_article_files[i]
                # articles_data.append(data)
        # except:
            # yaml file does not exist
            # print(f"Configuration file does not exist for {data_file}. Check README for info.")
    
    # print(list(zip(html_article_files, articles_data)))

    # add pygments css for code highlighting
    # # code_style = formatters.HtmlFormatter(style='dracula').get_style_defs('.codehilite')
    # try: 
    #     os.mkdir(build_path) 
    # except OSError as error: 
    #     print(error)
    # with open(os.path.join(build_path, 'codestyle.css'), 'w+') as css_file:
    #     css_file.write(code_style)

    site = Site.make_site(searchpath='src',
                          env_globals={'projects':project_data},
                          outpath=build_path,
                          contexts=[(r"articles/.*\.md", md_context_for_template), (r"articles/.*\.html", html_context), ('index.html', article_metadata)],
                          rules=[(r"articles/.*\.md", render_md), (r"articles/.*\.html", render_md)])
    site.render()
