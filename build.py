from staticjinja import Site
import yaml
import markdown2 as md
from pathlib import Path
import glob
import os
import argparse
import json

build_path = "./static"
html_article_dir = "articles/"
markdowner = md.Markdown()

def md_context(template):
    markdown_content = Path(template.filename).read_text()
    article_data = {"content": markdowner.convert(markdown_content)}
    metadata_file = os.path.splitext(template.filename)[0] + ".yml"
    try:
        with open(metadata_file, 'r') as f:
            metadata = yaml.load(f, Loader=yaml.Loader)
            article_data.update(metadata)
    except:
        print(f"Configuration file does not exist for {metadata_file}")

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
    md_file_dirs = sorted(glob.glob(os.path.join(article_dir, "*/")), key=os.path.getmtime)
    for i, dir in enumerate(md_file_dirs):
        data_file = glob.glob(os.path.join(dir, '*.yml'))[0]
        md_file = glob.glob(os.path.join(dir, '*.md'))
        if not md_file:
            # TODO: Max This is really lazy
            md_file = glob.glob(os.path.join(dir, '*.html'))[0]
        else:
            md_file = md_file[0]
        # try:
        with open(data_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)
            print(os.path.basename(os.path.split(dir)[0]))
            data["path"] = os.path.join("articles", os.path.basename(os.path.split(dir)[0]), os.path.basename(os.path.splitext(md_file)[0]) + '.html')
            articles_data.append(data)
        # except:
            # print(f"Configuration file does not exist for {data_file}. Check README for info.")
    print(articles_data)
    return {"articles": articles_data}

def render_md(site, template, **kwargs):
    out = site.outpath / Path(template.name).with_suffix(".html")
    os.makedirs(out.parent, exist_ok=True)
    site.get_template("article.html").stream(**kwargs).dump(str(out), encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build Site')
    parser.add_argument('--full', dest='full', default=False, action='store_true')

    args = parser.parse_args()
    # convert md pages to html
    # md_file_dirs = sorted(glob.glob(os.path.join(article_dir, "*/")), key=os.path.getmtime)
    # html_article_files = convertMDToHTML(md_file_dirs, builddir='src', outdir='/articles/', full=args.full)

    # build jinja templates
    with open('projects.json', 'r') as f:
        project_data = json.load(f)

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

    site = Site.make_site(searchpath='src',
                          env_globals={'projects':project_data},
                          outpath=build_path,
                          contexts=[(r"articles/.*\.md", md_context), (r"articles/.*\.html", html_context), ('index.html', article_metadata)],
                          rules=[(r"articles/.*\.md", render_md), (r"articles/.*\.html", render_md)])
    site.render()