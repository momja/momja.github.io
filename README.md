# My Personal Website
## How do I build the static site?
From the parent directory, run
```bash
> ./runBuild.sh
```

## Creating a new article
Articles should be placed in `.src/articles/article_name` the directory should contain...

if the articles is in html, two files:
1. markdown file with the article contents, and
2. yaml file with the metadata. A sample yaml file should like like the following

If the article is in markdown:
1. a single markdown file, with the metadata in the yaml header


```
title: "Study of ocean currents with physicalized models for interactive querying"
description: "A discussion on the growing field of physicalization, and its impact on tangible querying of geophysical data like ocean currents by seeding streamlines"
publish_date: YYYY-MM-dd

```

So the file structure is

```
articles
└── sample_article
    ├── sample_article.md
    └── sample_article.yml
```
