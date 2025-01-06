---
title: "Blog Challenge"
description: "From Bear Blog"
publish_date: 2025-01-06
tags: [100DaysToOffload, blog]
---
I was inspired by other bloggers to share my answers to the [bear blog questions](https://blog.avas.space/bear-blog-challenge/) ([Adapted by Kev](https://kevquirk.com/blog/blog-questions-challenge)). So here are my responses.

## Why did you start blogging in the first place?
I started my website in my last year of college as a way to place all my work from university and my brief stint in research in one place, so I can look back at and remember what I did. [Here](https://www.youtube.com/watch?v=VQgD2DCBnjQ) are [some](https://dl.acm.org/doi/10.1145/3488542) [examples](https://dizzard.net/articles/particle_simulation/particle_simulation.html). I don't do as much technically interesting things anymore, but as I started reading more of other's blogs, and getting on the [fediverse](https://fosstodon.org/@mjomdal), I became interested in sharing the projects I make, experiences I've had and lessons I've learned. In 2025, I've made [a resolution](https://dizzard.net/articles/resolutions/article.html) to really ramp up my blogging.

As another bonus, having blogs I can share with family and friends is really nice. If I want to [share a project](https://dizzard.net/articles/chest_of_drawers/article.html), or [how to make detergent](https://dizzard.net/articles/detergent/article.html), I just send a link to my blog post. It's a lot more fun than just sending a really long text.
## What platform are you using to manage your blog and why did you choose it?
Everything is hosted on Github Pages. I've cut my teeth at [Sequoia Fabrica](https://sequoiafabrica.org) self-hosting sites, and I also self-host a bunch of services behind Tailscale, So I'm sure I could figure out how to use a cloud provider to spin up my own hosting. But Github Pages is so damn easy, and it just works, so I don't see myself changing that for a while.

All posts are published to my blog through git. I push a new commit, and a Github action builds and pushes changes to another branch that holds just the static content for the site. Everything is in a public repository [here](https://github.com/momja/momja.github.io). There's a python script I wrote that will take all the blog posts, convert from Markdown to HTML, and copy them to a static directory. There are some improvements yet to be made, and I'll incrementally revise it. I'm not interested in an overhaul. Even though I know there's some issues, it works well enough. All the shiny cool tools like Hugo, 11ty, BearBlog, etc. seem like a lot of fun, but I kind of like knowing _all_ the steps from start to finish of how my blog gets published. Since the site is built as a bit of a playground for me, I prefer running it all myself.
## Have you blogged on other platforms before?
No. I published one article on Medium which is rather embarrassing and should be deleted. 
## How do you write your posts? For example, in a local editing tool, or in a panel/dashboard that's part of your blog?
I write either in Obsidian, or Vim. Usually, the first draft is in Obsidian, I'll copy and paste to my site's directory, and edit in Vim. It would be cool to build a custom web portal to publish to my site. My least favorite part of the workflow now is adding images because everything is placed in one resources folder, then I need to provide the markdown file with the correct relative path, and type the name of the image in correctly. It seems simple, but I always mess this part up. 
## When do you feel most inspired to write?
I don't have much written down on this site as of now. I'm trying to change that. I like writing in the morning before work sometimes, but usually it's just when I think of something to blog about. I really enjoy sharing projects big and small. When I finish a project, I like to share it.
## Do you publish immediately after writing, or do you let it simmer a bit as a draft?
No editing, no simmering, just press GO.
## What's your favorite post on your blog?
[My Favorite Things of 2024](https://dizzard.net/articles/favorite_things_2024/article.html). I wish more people would publish content like this. Stuff that's not YouTube affiliate, but actual tools, books, software that you liked using over the last year or so.

## Any future plans for your blog? Maybe a redesign, a move to another platform, or adding a new feature?
No redesigns in my future. If anything, I want to rip out some of the original stylistic decisions I've made so it is even more bare bones. The only future plan that I care about this year is publishing more content.

Oh! I suppose it _would_ be nice to publish from mobile. Rigging a solution for that might be on my 2025 roadmap.
