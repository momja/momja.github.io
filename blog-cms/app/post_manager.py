"""Blog post manager for CRUD operations."""
import os
import re
import glob
from datetime import datetime
from pathlib import Path
import frontmatter
import markdown2


class PostManager:
    """Manages blog post CRUD operations."""

    def __init__(self, articles_path):
        """Initialize post manager with articles directory path."""
        self.articles_path = articles_path

    def list_posts(self):
        """List all blog posts with metadata."""
        posts = []
        article_dirs = glob.glob(os.path.join(self.articles_path, "*/"))

        for article_dir in article_dirs:
            # Find markdown file in directory
            md_files = glob.glob(os.path.join(article_dir, "*.md"))
            if not md_files:
                continue

            md_file = md_files[0]

            try:
                post = frontmatter.load(md_file)

                post_data = {
                    'slug': os.path.basename(os.path.dirname(md_file)),
                    'title': post.get('title', 'Untitled'),
                    'description': post.get('description', ''),
                    'publish_date': post.get('publish_date'),
                    'file_path': md_file,
                    'content': post.content
                }

                posts.append(post_data)
            except Exception as e:
                print(f"Error reading {md_file}: {e}")
                continue

        # Sort by publish date (newest first)
        posts.sort(key=lambda x: x.get('publish_date') or datetime.min, reverse=True)

        return posts

    def get_post(self, slug):
        """Get a single post by slug."""
        article_dir = os.path.join(self.articles_path, slug)

        if not os.path.exists(article_dir):
            return None

        # Find markdown file
        md_files = glob.glob(os.path.join(article_dir, "*.md"))
        if not md_files:
            return None

        md_file = md_files[0]

        try:
            post = frontmatter.load(md_file)

            return {
                'slug': slug,
                'title': post.get('title', 'Untitled'),
                'description': post.get('description', ''),
                'publish_date': post.get('publish_date'),
                'file_path': md_file,
                'content': post.content,
                'metadata': post.metadata
            }
        except Exception as e:
            print(f"Error reading post: {e}")
            return None

    def create_post(self, slug, title, description, content, publish_date=None):
        """Create a new blog post."""
        # Create slug-safe directory name
        safe_slug = re.sub(r'[^a-z0-9_-]', '_', slug.lower())
        article_dir = os.path.join(self.articles_path, safe_slug)

        # Create directory
        os.makedirs(article_dir, exist_ok=True)

        # Create markdown file
        md_file = os.path.join(article_dir, "article.md")

        # Create post with frontmatter
        post = frontmatter.Post(content)
        post['title'] = title
        post['description'] = description
        post['publish_date'] = publish_date or datetime.now().strftime('%Y-%m-%d')

        # Write file
        with open(md_file, 'w') as f:
            f.write(frontmatter.dumps(post))

        return {
            'slug': safe_slug,
            'file_path': md_file,
            'title': title
        }

    def update_post(self, slug, title, description, content, publish_date):
        """Update an existing blog post."""
        post_data = self.get_post(slug)

        if not post_data:
            return False, "Post not found"

        md_file = post_data['file_path']

        # Update post
        post = frontmatter.Post(content)
        post['title'] = title
        post['description'] = description
        post['publish_date'] = publish_date

        # Write updated file
        with open(md_file, 'w') as f:
            f.write(frontmatter.dumps(post))

        return True, "Post updated successfully"

    def delete_post(self, slug):
        """Delete a blog post."""
        article_dir = os.path.join(self.articles_path, slug)

        if not os.path.exists(article_dir):
            return False, "Post not found"

        # Remove directory and all contents
        import shutil
        shutil.rmtree(article_dir)

        return True, "Post deleted successfully"

    def render_preview(self, content):
        """Render markdown content to HTML for preview."""
        markdowner = markdown2.Markdown(
            extras={
                'fenced-code-blocks': None,
                'html-classes': {
                    'code': 'codeblock',
                    'pre': 'codewrapper',
                    'ol': 'list-decimal'
                },
                'cuddled-lists': None
            },
            safe_mode=False
        )

        return markdowner.convert(content)

    def save_image(self, slug, image_file):
        """Save an uploaded image for a blog post."""
        article_dir = os.path.join(self.articles_path, slug)

        # Ensure article directory exists
        os.makedirs(article_dir, exist_ok=True)

        # Save image to images directory (global)
        images_dir = os.path.join(os.path.dirname(self.articles_path), '..', 'images')
        os.makedirs(images_dir, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{slug}_{timestamp}_{image_file.filename}"
        filepath = os.path.join(images_dir, filename)

        # Save file
        image_file.save(filepath)

        # Return relative path for markdown
        return f"../images/{filename}"
