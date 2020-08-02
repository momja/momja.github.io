import markdown2 as md
import glob
import os

# Open up files in blog directory
markdowner = md.Markdown()

md_files = glob.glob("./posts_md/*.md")
for md_file in md_files:
    basename = os.path.splitext(os.path.basename(md_file))[0]
    with open(md_file, 'r') as f:
        file_str = f.read()
        html = markdowner.convert(file_str)
        # write files to blog
        new_filepath = os.path.join("./posts/", basename + ".html")
        with open(new_filepath, "w") as new_f:
            new_f.write(html)
