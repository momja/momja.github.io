---
title: Deploy Github Pages with Jinja and Github Actions
description: Github Pages with Jinja and TailwindCSS
publish_date: 2022-06-14
---


This blog, like many others is hosted on [Github Pages](https://pages.github.com/). Github Pages is a great (and free) way to post small static sites like personal websites. The annoying thing is that you have to push build code that would _usually_ be included in your `.gitignore` file. So if you don't want to have to build your site locally, and include the build files in your repository, there is an option for you that leverages Github Actions.

Now, if you haven't heard of [Github Actions](https://github.com/features/actions), you should check it out. It's Github's platform for CI/CD, and it's easily configurable with .yaml files. There's nothing special you have to do for a repository, you just include the action files in the `.github/workflows` directory.

[My site repository](https://github.com/momja/momja.github.io) is currently being deployed with a [github action](https://github.com/JamesIves/github-pages-deploy-action) written by [`@JamesIves`](https://github.com/JamesIves). The sample `.yaml` file looks like this:

```yaml
name: Build and Deploy
on: [push]
permissions: 
  contents: write
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout 🛎️
        uses: actions/checkout@v3

      - name: Install and Build 🔧
        run: |
          npm ci
          npm run build

      - name: Deploy 🚀
        uses: JamesIves/github-pages-deploy-action@v4.3.3
        with:
          branch: gh-pages
          folder: build
```

There's very little here we have to change to get this working for us.

1. First, make sure this section matches the branch your github site is hosted on. You can check which branch is currently used by opening your github pages repository then:

    Settings -> Code and Automation -> Pages -> Source.

    ```yaml
    with:
        branch: gh-pages <- make sure this matches "branch"
        folder: build
    ```
    ![../../images/setting-gh-pages.png](../../images/setting-gh-pages.png)

2. Now we need to update the "Install and Build 🔧" section. There are a couple things we have to do for this to work, and it will vary for you depending on how your site is being built. I'm generating the static pages of my site using the Jinja web templating engine, and then I inject style with Postcss and Tailwind. This means I need to run a python script to generate the HTML files, then run a postcss injection to transform my css. I've got [all this configured](https://github.com/momja/momja.github.io/blob/master/package.json) in my 'package.json' file, so whenever I run `npm run build`, all this is taken care of. At least that all happens smoothly locally. When running this on some ephemeral virtual machine, you have to actually make sure all the dependencies are downloaded first. For the postcss dependencies, that's as simple as running `npm install` assuming you've correctly set up your packages.

    For Python, it is a little different. I'm not the biggest fan of dependency management in Python, but I recently came across a tool called [pipreqs](https://github.com/bndr/pipreqs) which solves the challenges I associate with generating package requirements for Python. To build a requirements.txt file with pipreqs, just run `pipreqs` in your project directory. You will want to include this requirements file in your git commit, because we will then use it to install all the pip dependencies on the VM used by Github Actions!

    ```yaml
    - name: Install and Build 🔧
      run: |
        npm ci
        npm run build
    ```
    
    becomes:

    ```yaml
    - name: Install and Build 🔧
      run: |
        pip install -r requirements.txt
        npm install
        npm run build
    ```

3. Lastly, I didn't want the `gh-pages` branch to be updated each time a change is made to _any_ branch, so I changed the yaml field at the top of the file for when the action should be triggered:
  
    ```yaml
    on: [push]
    ```

    becomes:

    ```yaml
    on:
        push:
            branches:
                - master
    ```

And there you have it! Check out the final file [here](https://github.com/momja/momja.github.io/blob/38e1a2985c1983cbd35c07d970318d8743cb63ba/.github/workflows/deploy-to-gh-pages.yml)
