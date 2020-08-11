import markdown2 as md
import glob
import os

def convertMDToHTML(md_files):
    # Open up files in blog directory
    markdowner = md.Markdown()

    for md_file in md_files:
        basename = os.path.splitext(os.path.basename(md_file))[0]
        new_filepath = os.path.join("./posts/", basename + ".html")
        # only build for new files
        if (os.path.exists(new_filepath)):
            continue
        with open(md_file, 'r') as f:
            file_str = f.read()
            html = markdowner.convert(file_str)
            # write files to blog
            with open(new_filepath, "w") as new_f:
                new_f.write(html)
