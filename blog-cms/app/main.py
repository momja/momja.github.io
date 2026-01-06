"""Flask application for blog CMS."""
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
from git_manager import GitManager
from post_manager import PostManager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
REPO_PATH = os.environ.get('REPO_PATH', '/repo')
ARTICLES_PATH = os.path.join(REPO_PATH, 'src', 'articles')

# Initialize managers
git_manager = GitManager(REPO_PATH)
post_manager = PostManager(ARTICLES_PATH)

# Simple authentication (enhance with proper auth in production)
USERNAME = os.environ.get('CMS_USERNAME', 'admin')
PASSWORD = os.environ.get('CMS_PASSWORD', 'changeme')


def require_auth(f):
    """Decorator to require authentication."""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout."""
    session.pop('authenticated', None)
    return redirect(url_for('login'))


@app.route('/')
@require_auth
def index():
    """List all blog posts."""
    posts = post_manager.list_posts()
    current_branch = git_manager.get_current_branch()
    unpublished_branches = git_manager.get_unpublished_branches()

    return render_template('index.html',
                           posts=posts,
                           current_branch=current_branch,
                           unpublished_branches=unpublished_branches)


@app.route('/new', methods=['GET'])
@require_auth
def new_post():
    """Create new post page."""
    return render_template('editor.html', post=None, mode='new')


@app.route('/edit/<slug>', methods=['GET'])
@require_auth
def edit_post(slug):
    """Edit existing post page."""
    # Try to get the post from current branch
    post = post_manager.get_post(slug)

    # If not found, check if there's an unpublished branch for this post
    if not post:
        branch_name = f"blog/{slug}"

        # Check if the branch exists
        if branch_name in git_manager.list_branches():
            # Checkout the branch to access the post
            success, message = git_manager.checkout_branch(branch_name)

            if success:
                # Try to get the post again from the checked out branch
                post = post_manager.get_post(slug)

    if not post:
        return "Post not found", 404

    return render_template('editor.html', post=post, mode='edit')


@app.route('/preview/<slug>', methods=['GET'])
@require_auth
def preview_post(slug):
    """Preview post as it will appear on blog."""
    # Try to get the post from current branch
    post = post_manager.get_post(slug)

    # If not found, check if there's an unpublished branch for this post
    if not post:
        branch_name = f"blog/{slug}"

        # Check if the branch exists
        if branch_name in git_manager.list_branches():
            # Checkout the branch to access the post
            success, message = git_manager.checkout_branch(branch_name)

            if success:
                # Try to get the post again from the checked out branch
                post = post_manager.get_post(slug)

    if not post:
        return "Post not found", 404

    # Render markdown to HTML
    html_content = post_manager.render_preview(post['content'])

    return render_template('preview.html',
                           title=post['title'],
                           content=html_content,
                           publish_date=post['publish_date'])


@app.route('/api/posts', methods=['POST'])
@require_auth
def create_post_api():
    """API endpoint to create a new post."""
    data = request.json

    slug = data.get('slug')
    title = data.get('title')
    description = data.get('description')
    content = data.get('content')
    publish_date = data.get('publish_date')

    if not all([slug, title, description, content]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create branch for this post
        branch_name = f"blog/{slug}"
        success, message = git_manager.create_branch(branch_name)

        if not success:
            return jsonify({'error': message}), 500

        # Create post
        post_data = post_manager.create_post(slug, title, description, content, publish_date)

        # Commit changes
        commit_message = f"Add new blog post: {title}"
        success, message = git_manager.commit_changes([post_data['file_path']], commit_message)

        if not success:
            return jsonify({'error': message}), 500

        return jsonify({
            'success': True,
            'slug': post_data['slug'],
            'branch': branch_name,
            'message': 'Post created successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/posts/<slug>', methods=['PUT'])
@require_auth
def update_post_api(slug):
    """API endpoint to update a post."""
    data = request.json

    title = data.get('title')
    description = data.get('description')
    content = data.get('content')
    publish_date = data.get('publish_date')

    if not all([title, description, content]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        success, message = post_manager.update_post(slug, title, description, content, publish_date)

        if not success:
            return jsonify({'error': message}), 400

        # Commit changes
        post = post_manager.get_post(slug)
        commit_message = f"Update blog post: {title}"
        git_manager.commit_changes([post['file_path']], commit_message)

        return jsonify({
            'success': True,
            'message': 'Post updated successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/posts/<slug>', methods=['DELETE'])
@require_auth
def delete_post_api(slug):
    """API endpoint to delete a post."""
    try:
        # Delete the post files
        success, message = post_manager.delete_post(slug)

        if not success:
            return jsonify({'error': message}), 400

        # Delete the associated branch if it exists
        branch_name = f"blog/{slug}"
        if branch_name in git_manager.list_branches():
            git_manager.delete_branch(branch_name, force=True)

        return jsonify({
            'success': True,
            'message': 'Post and branch deleted successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-image', methods=['POST'])
@require_auth
def upload_image():
    """API endpoint to upload an image."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    image = request.files['image']
    slug = request.form.get('slug', 'general')

    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image_path = post_manager.save_image(slug, image)

        return jsonify({
            'success': True,
            'path': image_path,
            'message': 'Image uploaded successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/publish/<slug>', methods=['POST'])
@require_auth
def publish_post(slug):
    """Publish a post by merging to master and pushing."""
    try:
        current_branch = git_manager.get_current_branch()

        # If not on the post's branch, checkout
        branch_name = f"blog/{slug}"
        if current_branch != branch_name:
            success, message = git_manager.checkout_branch(branch_name)
            if not success:
                return jsonify({'error': f'Branch not found: {message}'}), 400

        # Merge to master
        success, message = git_manager.merge_to_master(branch_name)
        if not success:
            return jsonify({'error': message}), 500

        # Push to remote
        success, message = git_manager.push_to_remote('master')
        if not success:
            return jsonify({'error': message}), 500

        return jsonify({
            'success': True,
            'message': 'Post published successfully. GitHub Actions will deploy it.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/preview', methods=['POST'])
@require_auth
def preview_markdown():
    """API endpoint to preview markdown as HTML."""
    data = request.json
    content = data.get('content', '')

    html = post_manager.render_preview(content)

    return jsonify({
        'success': True,
        'html': html
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('DEBUG', 'False') == 'True')
