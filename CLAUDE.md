# CLAUDE.md - AI Assistant Guide for momja.github.io

## Repository Overview

This is a personal portfolio and blog website for Maxwell Omdal (dizzard.net), built as a static site generator using Python, Jinja2 templates, and Tailwind CSS. The site is deployed to GitHub Pages and features blog articles, project showcases, and an RSS feed.

**Owner:** Maxwell Omdal
**Website:** http://dizzard.net
**GitHub:** https://github.com/momja
**Domain:** Custom domain via CNAME

## Architecture

### Technology Stack

- **Static Site Generator:** Custom Python build system using `staticjinja`
- **Templating:** Jinja2 templates with custom contexts
- **Content Format:** Markdown with YAML frontmatter (supports both `.md` and `.html` articles)
- **Styling:** Tailwind CSS v3 with Typography plugin
- **Deployment:** GitHub Actions → GitHub Pages (`gh-pages` branch)
- **Analytics:** GoatCounter (privacy-focused)
- **Code Highlighting:** Pygments with Dracula theme

### Build Process Flow

1. **Python Build (`build.py`):**
   - Parses all articles from `src/articles/*/` directories
   - Converts Markdown to HTML using `markdown2`
   - Extracts metadata from YAML frontmatter or separate `.yml` files
   - Renders Jinja2 templates with article and project contexts
   - Generates syntax highlighting CSS
   - Outputs to `static/` directory

2. **Asset Processing (`runBuild.sh`):**
   - Runs Python build script
   - Compiles Tailwind CSS via PostCSS
   - Copies static assets (images, PDFs, videos, favicon)
   - Generates RSS feed
   - (Optional) Image resizing with ImageMagick (currently commented out)

3. **Deployment (`.github/workflows/deploy-to-gh-pages.yml`):**
   - Triggers on push to `master` branch
   - Installs dependencies (Python, npm, ImageMagick)
   - Runs build process
   - Deploys `static/` folder to `gh-pages` branch

## Directory Structure

```
momja.github.io/
├── .github/
│   └── workflows/
│       └── deploy-to-gh-pages.yml    # GitHub Actions deployment config
├── article_template/
│   └── article.md                     # Template for new articles
├── favicon/                           # Favicon files (various sizes)
├── images/                            # All site images and media
├── src/                               # Source files for site generation
│   ├── articles/                      # Blog article directories
│   │   ├── article_name/
│   │   │   ├── article.md            # Article content with frontmatter
│   │   │   ├── article.yml           # (Optional) Separate metadata
│   │   │   └── *.{jpg,png,gif}       # Article-specific images
│   ├── helper_templates/              # Jinja2 partial templates
│   │   ├── _article.html             # Article page layout
│   │   ├── _article_listings.html    # Article cards for index
│   │   ├── _project_card.html        # Project card component
│   │   ├── _projects.html            # Projects section
│   │   └── _theme_toggle.html        # Dark mode toggle
│   ├── index.html                     # Main landing page template
│   └── mastodon.html                  # Mastodon verification page
├── style/
│   └── tailwind.css                   # Tailwind input file
├── static/                            # Build output (gitignored)
│   └── ...                            # Generated HTML, CSS, assets
├── build.py                           # Main build script
├── convertMDToHTML.py                 # Utility for markdown conversion
├── projectJSONParser.py               # Parses projects.json with date handling
├── runBuild.sh                        # Build orchestration script
├── projects.json                      # Project portfolio data
├── package.json                       # npm dependencies (Tailwind, PostCSS)
├── requirements.txt                   # Python dependencies
├── postcss.config.js                  # PostCSS configuration
├── tailwind.config.js                 # Tailwind configuration
├── CNAME                              # Custom domain configuration
├── .gitignore                         # Git ignore rules
└── README.md                          # Basic build instructions
```

## Key Files and Their Purposes

### Build System

#### `build.py` (273 lines)
Main build orchestration script. Key functions:

- `md_context(filename, include_content)`: Extracts metadata and content from Markdown files
- `md_context_for_template(template)`: Wrapper for template-based context generation
- `html_context(template)`: Handles HTML articles with separate YAML metadata
- `article_metadata(template)`: Aggregates all articles, sorts by publish date
- `render_md(site, template, **kwargs)`: Renders Markdown as HTML using `_article.html` template
- `generate_rss()`: Creates RSS 2.0 feed from articles
- `replace_img_src(m)`: Rewrites image paths for production (prepends base URL)

**Important Notes:**
- Uses frontmatter-style metadata (YAML header) OR separate `.yml` files
- Image paths are rewritten in production builds (`../images/` → `http://dizzard.net/images/`)
- Development mode (`--dev` flag) preserves relative paths
- Automatically converts PNG to JPG in image links
- Sorts articles by `publish_date` in reverse chronological order

#### `runBuild.sh`
Bash script that orchestrates the full build:
1. Runs `build.py` with optional `--dev` flag
2. Compiles Tailwind CSS via PostCSS
3. Copies static assets (PDFs, videos, favicon)
4. Copies RSS feed to static directory
5. (Commented out) Image resizing with ImageMagick

#### `projectJSONParser.py`
Parses `projects.json` with custom date handling:
- Converts `start_date` and `end_date` strings to datetime objects
- Formats display dates as "Mon YY — Mon YY"
- Sorts projects by start date (newest first)

### Content Files

#### `projects.json`
Array of project objects with structure:
```json
{
  "name": "Project Name",
  "start_date": "MM/YY",
  "end_date": "MM/YY",
  "image_path": "images/project.jpg",
  "description": "Project description (HTML allowed)",
  "url": "https://project-url.com"
}
```

#### Article Structure (Two Formats)

**Format 1: Markdown with Frontmatter** (Preferred)
```markdown
---
title: "Article Title"
description: "Article description for meta tags and listings"
publish_date: YYYY-MM-DD
---

# Article Title
Article content in Markdown...
```

**Format 2: Separate HTML/Markdown + YAML**
```yaml
# article.yml
title: "Article Title"
description: "Article description"
publish_date: YYYY-MM-DD
```

```html
<!-- article.html or article.md -->
<div>Article content...</div>
```

### Templates

#### `src/helper_templates/_article.html`
Layout template for individual articles:
- Includes Tailwind CSS and Pygments code highlighting
- GoatCounter analytics integration
- Dark mode support
- Back button navigation
- Responsive typography (`prose lg:prose-xl`)

#### `src/index.html`
Main landing page with:
- Personal bio and social links
- Article listings (via `_article_listings.html`)
- Project showcases (via `_projects.html`)
- Dark mode support

## Development Workflows

### Local Development

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Development build (preserves relative paths)
npm run build:dev
# OR
./runBuild.sh --dev

# Production build
npm run build
# OR
./runBuild.sh

# View locally
# Output: file:///path/to/static/index.html
```

### Creating a New Article

1. **Create article directory:**
   ```bash
   mkdir src/articles/article_name
   ```

2. **Use template:**
   ```bash
   cp article_template/article.md src/articles/article_name/article.md
   ```

3. **Edit frontmatter:**
   ```markdown
   ---
   title: "Your Article Title"
   description: "A compelling description for SEO and RSS"
   publish_date: 2024-01-15
   ---

   # Your Article Title
   Content goes here...
   ```

4. **Add images (optional):**
   - Place images in `images/` directory (not in article folder)
   - Reference in Markdown: `![Alt text](../images/image.jpg)`
   - Build process rewrites paths for production

5. **Test locally:**
   ```bash
   npm run build:dev
   ```

6. **Commit and push:**
   ```bash
   git add src/articles/article_name/
   git commit -m "Add new article: Your Article Title"
   git push origin master
   ```
   - GitHub Actions automatically builds and deploys

### Adding a New Project

1. **Edit `projects.json`:**
   ```json
   {
     "name": "New Project",
     "start_date": "01/24",
     "end_date": "03/24",
     "image_path": "images/project.jpg",
     "description": "Project description",
     "url": "https://project-url.com"
   }
   ```

2. **Add project image:**
   - Place in `images/` directory
   - Recommended size: 720x720 or similar aspect ratio

3. **Build and deploy:**
   - Automatic on push to `master` branch

## Key Conventions and Guidelines

### Article Conventions

1. **Naming:**
   - Directory names: lowercase, underscores (e.g., `my_article_name`)
   - Markdown file: `article.md` (preferred naming convention)
   - Alternative naming: Match directory name (e.g., `my_article.md`)

2. **Dates:**
   - Format: `YYYY-MM-DD` (ISO 8601)
   - Must be parseable by Python's datetime
   - Used for sorting and RSS feed

3. **Images:**
   - Store in top-level `images/` directory
   - Reference with relative path: `../images/filename.jpg`
   - Build process handles path rewriting
   - PNG references auto-converted to JPG in production

4. **Code Blocks:**
   - Use fenced code blocks with language specifiers
   - Pygments handles syntax highlighting
   - Dracula theme applied automatically

5. **Markdown Features:**
   - Enabled extras: `fenced-code-blocks`, `html-classes`, `cuddled-lists`
   - Custom classes: `.codeblock`, `.codewrapper`, `.list-decimal`
   - Raw HTML allowed (safe_mode=False)

### Git Workflow

1. **Development Branch:** `master`
2. **Deployment Branch:** `gh-pages` (auto-managed by GitHub Actions)
3. **Protected Files:** `static/`, `node_modules/`, `__pycache__/`
4. **Feature Branches:** Not required for articles, but recommended for major changes

### Build Artifacts

**Gitignored (Never Commit):**
- `static/` - Build output directory
- `node_modules/` - npm dependencies
- `__pycache__/` - Python bytecode
- `rss.xml` - Generated feed (root level)
- `CLAUDE.md` - This file

**Committed:**
- All source files in `src/`
- Configuration files (`package.json`, `requirements.txt`, etc.)
- `images/` directory with all media
- `projects.json`

## Dependencies

### Python (requirements.txt)

```
docopt-ng==0.9.0          # CLI parsing (unused currently)
easywatch==0.0.5          # File watching (unused currently)
feedgen==1.0.0            # RSS feed generation
feedgenerator==2.1.0      # RSS feed generation
Jinja2==3.1.3             # Template engine
lxml==5.2.1               # XML processing
markdown2==2.4.13         # Markdown to HTML conversion
MarkupSafe==2.1.5         # Jinja2 dependency
numpy==1.26.4             # Numeric operations (unused currently)
opencv-python==4.5.5.64   # Image processing (unused currently)
Pygments==2.13.0          # Syntax highlighting
python-dateutil==2.9.0    # Date parsing
python-frontmatter==1.0.0 # YAML frontmatter parsing
pytz==2024.1              # Timezone handling
PyYAML==6.0.1             # YAML parsing
six==1.16.0               # Python 2/3 compatibility
staticjinja==4.1.3        # Static site generation
watchdog==4.0.0           # File system monitoring
```

### Node.js (package.json)

```json
{
  "dependencies": {
    "lodash": "^4.17.21",
    "minimist": "^1.2.6"
  },
  "devDependencies": {
    "@fortawesome/fontawesome-free": "^5.15.4",
    "@tailwindcss/typography": "^0.5.7",
    "autoprefixer": "^10.4.7",
    "postcss": "^8.4.31",
    "postcss-cli": "^9.1.0",
    "tailwindcss": "^3.0.24"
  }
}
```

## Styling System

### Tailwind CSS

**Configuration (`tailwind.config.js`):**
- Content paths: `./static/**/*.{html,js}`
- Plugins: `@tailwindcss/typography`
- Theme: Extended default theme

**Custom Classes:**
- `.paper-texture` - Background texture effect
- `.paper-texture-text` - Text styling for paper effect
- `.prose` - Typography plugin for article content
- `.dark:*` - Dark mode variants

**Color Scheme:**
- Light: `bg-yellow-50` (paper-like)
- Dark: `bg-slate-800`
- Accent: Indigo palette (`indigo-800`, `indigo-50`, etc.)

### Code Highlighting

- **Library:** Pygments
- **Theme:** Dracula
- **Output:** `static/codestyle.css`
- **Classes:** `.codehilite` for highlighted code blocks

## Deployment

### GitHub Actions Workflow

**Trigger:** Push to `master` branch

**Steps:**
1. Checkout repository
2. Install ImageMagick (system dependency)
3. Install Python dependencies (`pip install -r requirements.txt`)
4. Install Node dependencies (`npm install`)
5. Run build (`npm run build`)
6. Deploy `static/` folder to `gh-pages` branch

**Deployment Time:** ~2-3 minutes

### GitHub Pages Configuration

- **Source Branch:** `gh-pages`
- **Custom Domain:** Configured via `CNAME` file
- **Base URL:** `http://dizzard.net/`
- **SSL:** Automatic via GitHub Pages

## Testing and Debugging

### Local Testing

```bash
# Development build with relative paths
./runBuild.sh --dev

# Open in browser
open static/index.html

# Or use Python server
cd static && python -m http.server 8000
```

### Common Issues

1. **Article not appearing:**
   - Check `publish_date` is valid YAML date format
   - Ensure frontmatter or `.yml` file exists
   - Verify directory structure: `src/articles/name/article.md`

2. **Images not loading:**
   - In dev mode: Use relative paths (`../images/`)
   - In production: Paths auto-rewritten to absolute URLs
   - Check image exists in `images/` directory

3. **Build failures:**
   - Check Python syntax in `build.py`
   - Verify all dependencies installed
   - Look for YAML parsing errors in articles

4. **CSS not applying:**
   - Rebuild Tailwind: `postcss style/tailwind.css -o static/tailwind.css`
   - Check `tailwind.config.js` content paths
   - Purge might remove used classes if not in content paths

### Debug Mode

Build script supports `--dev` flag for development:
- Preserves relative image paths
- Outputs to `static/` directory
- No image optimization (faster builds)

## RSS Feed

**Generated File:** `rss.xml` (copied to `static/rss.xml`)

**Format:** RSS 2.0

**Features:**
- Includes all published articles
- Full article content in `<description>` (CDATA wrapped)
- Unique IDs based on article index
- Author: Maxwell Omdal
- Sorted by publish date (newest first)

**Feed URL:** `http://dizzard.net/rss.xml`

## Analytics and Tracking

**Service:** GoatCounter
**URL:** `https://dizzard.goatcounter.com/count`
**Privacy:** No cookies, GDPR-friendly
**Enabled on:** All pages (including articles)

## External Integrations

- **Font Awesome:** Kit integration for icons
- **GoatCounter:** Privacy-focused analytics
- **Mastodon:** Profile verification via `rel="me"` link

## AI Assistant Guidelines

### When Making Changes

1. **Always read existing code first** - Never modify files without understanding current implementation
2. **Preserve existing patterns** - Match the coding style and conventions already in use
3. **Test locally before committing** - Run `./runBuild.sh --dev` and verify output
4. **Don't over-engineer** - Keep solutions simple and focused on the request
5. **Respect the build system** - Don't bypass or modify core build logic without good reason

### Common Tasks

**Adding an article:**
- Use `article_template/article.md` as starting point
- Always include frontmatter with title, description, publish_date
- Place in `src/articles/article_name/` directory

**Modifying templates:**
- Jinja2 templates in `src/` and `src/helper_templates/`
- Test changes with multiple articles to ensure consistency
- Preserve existing classes and structure

**Updating dependencies:**
- Document reasons for updates
- Test build process after updates
- Update both `requirements.txt` and `package.json` if needed

### What NOT to Do

1. **Don't commit build artifacts** - Never commit `static/` directory
2. **Don't hardcode paths** - Use relative paths or configuration
3. **Don't skip frontmatter** - All articles need metadata
4. **Don't break RSS feed** - Test feed generation after article changes
5. **Don't remove analytics** - GoatCounter is intentionally privacy-focused
6. **Don't modify `.gitignore`** - Build artifacts must stay ignored

### Security Considerations

- No user input processing (static site)
- No backend or database
- YAML parsing uses safe loader
- HTML sanitization disabled (trusted content only)
- External scripts limited to analytics and Font Awesome

## Maintenance Notes

### Regular Maintenance Tasks

1. **Dependency Updates:**
   - Check for security updates monthly
   - Test build process after updates
   - Update Python and Node dependencies separately

2. **Image Optimization:**
   - ImageMagick resize commented out in `runBuild.sh`
   - Consider enabling for large image sets
   - Current approach: manual optimization before upload

3. **RSS Feed Validation:**
   - Validate at https://validator.w3.org/feed/
   - Check after structural changes to articles

### Future Improvements (Ideas)

- Enable image optimization in build process
- Add dark mode toggle UI (template exists but unused)
- Implement proper watching for development
- Add TypeScript for client-side scripts
- Consider static search functionality
- Pagination for article listings

## Contact and Support

**Repository Owner:** Maxwell Omdal
**Email:** mjomdal@gmail.com
**GitHub:** https://github.com/momja
**Mastodon:** https://fosstodon.org/@mjomdal

For AI assistants: When in doubt, check existing articles and templates for patterns before implementing new features.
