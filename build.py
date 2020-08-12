from staticjinja import Site
import yaml
from convertMDToHTML import convertMDToHTML
import glob
import os
import argparse

build_path = "./build"
html_article_path = os.path.join(build_path, "articles/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build Site')
    parser.add_argument('--full', dest='full', default=False, action='store_true')

    args = parser.parse_args()
    article_dir = "./articles/"
    # convert md pages to html
    md_file_dirs = sorted(glob.glob(os.path.join(article_dir, "*/")), key=os.path.getmtime)
    html_article_files = convertMDToHTML(md_file_dirs, outdir=html_article_path, full=args.full)

    # build jinja templates
    dummy_data = [
        {'name': 'Image-Based Tracking for AR Physicalizations', 'date': '04/20 - NOW', 'image_path': 'images/ar_localization.png'},
        {'name': 'CPU Raytracer', 'date': '01/20 - 03/20', 'image_path': 'images/raytracer.jpg'},
        {'name': 'A Comparison of CycleGAN and DualGAN for Painterly Effects', 'data': '01/19 - 05/19', 'image_path': 'images/GAN.jpg'},
        {'name': 'Slope One Algorithm For Yelp Rating Predictions', 'date': '01/20 - 03/20', 'image_path': 'images/avg_rating_per_user.jpg'},
        {'name': 'Bucketz, an iOS Game Built With Swift', 'date': '06/17 - 08/17', 'image_path': 'images/bucketz2.jpg'},
        {'name': 'DineDice: A Randomized Local Restaurant Recommender', 'date': '01/17 - 02/17', 'image_path': 'images/dinedice_logo.png'},
        {'name': 'Path Planning Game', 'date': '06/20 - 07/20', 'image_path': 'projects/path_planning/images/header.png'},
        {'name': 'Particle Simulation', 'date': '07/20 - 08/20', 'image_path': 'projects/particle_simulation/images/smokestack.png'}
    ]

    # Pair every html articl with its YAML file
    article_data = []
    for i, dir in enumerate(md_file_dirs):
        data_file = glob.glob(os.path.join(dir, '*.yml'))[0]
        with open(data_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.Loader)
            print(data_file)
            print(html_article_files)
            data["path"] = html_article_files[i]
            article_data.append(data)


    site = Site.make_site(env_globals={'projects':dummy_data, 'articles': article_data},
                          outpath=build_path,
                          contexts=list(zip(html_article_files, article_data)))
    site.render(use_reloader=True)