import markdown2 as md
import glob
import os

def convertMDToHTML(md_dirs, builddir='./src', outdir='./', full=False):
    """
    Converts Markdown files to HTML.

    Args:
        md_dirs (list): List of directories containing Markdown files.
        builddir (str, optional): Base directory for output. Defaults to './src'.
        outdir (str, optional): Output directory for HTML files. Defaults to './'.
        full (bool, optional): If True, rebuild all files; if False, only build where there isn't already a .html. Defaults to False.

    Returns:
        list: Paths to newly created HTML files.
    """
    # Open up files in blog directory
    markdowner = md.Markdown()

    new_files = []
    os.makedirs(outdir, exist_ok=True)

    for folder in md_dirs:
        md_file = glob.glob(os.path.join(folder, "*.md"))[0]
        basename = os.path.splitext(os.path.basename(md_file))[0]
        new_filepath = os.path.join(builddir, outdir, basename + ".html")
        # only build for new files
        if (not full and os.path.exists(new_filepath)):
            continue
        with open(md_file, 'r') as f:
            file_str = f.read()
            html = markdowner.convert(file_str)
            # write files to blog
            with open(new_filepath, "w+") as new_f:
                new_f.write(html)
        new_files.append(os.path.join(outdir, basename + ".html"))

    return new_files
