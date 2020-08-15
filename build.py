from staticjinja import Site
import yaml
from convertMDToHTML import convertMDToHTML
import glob
import os
import argparse
import json

build_path = "./static"
html_article_dir = "articles/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build Site')
    parser.add_argument('--full', dest='full', default=False, action='store_true')

    args = parser.parse_args()
    article_dir = "./articles/"
    # convert md pages to html
    md_file_dirs = sorted(glob.glob(os.path.join(article_dir, "*/")), key=os.path.getmtime)
    html_article_files = convertMDToHTML(md_file_dirs, builddir=build_path, outdir=html_article_dir, full=args.full)

    # build jinja templates
    with open('projects.json', 'r') as f:
        project_data = json.load(f)

    # Pair every html article with its YAML file
    article_data = []
    for i, dir in enumerate(md_file_dirs):
        data_file = glob.glob(os.path.join(dir, '*.yml'))[0]
        with open(data_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)
            print(data_file)
            data["path"] = html_article_files[i]
            article_data.append(data)


    site = Site.make_site(env_globals={'projects':project_data, 'articles': article_data},
                          outpath=build_path,
                          contexts=list(zip(html_article_files, article_data)))
    site.render()