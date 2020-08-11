import jinja2
from staticjinja import Site
from convertMDToHTML import convertMDToHTML
import glob
import os

if __name__ == "__main__":
    # convert md pages to html
    md_files = glob.glob("./posts_md/*.md")
    convertMDToHTML(md_files)

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

    site = Site.make_site(env_globals={'projects':dummy_data})
    site.render(use_reloader=True)

    # file_loader = jinja2.FileSystemLoader('templates/')
    # for file in glob.glob('templates/*'):
    #     env = jinja2.Environment(loader=file_loader)
    #     template = env.get_template('index.j2')
    #     output = template.render(projects = dummy_data)
    #     basename = os.path.basename(os.path.splitext(file))
    #     with open(os.path.join('build', basename, '.html'), 'w') as fh:
    #         fh.write(output)

    