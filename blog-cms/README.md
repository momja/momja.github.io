# Blog CMS - Self-Hosted Content Management System

A lightweight, git-integrated CMS for managing your static blog. Features a mobile-friendly WYSIWYG editor, automatic git operations, and Docker deployment with Traefik support.

## Features

- ✍️ **WYSIWYG Editor** - Quill-based rich text editor with markdown support
- 📱 **Mobile-Friendly** - Responsive design with mobile image capture support
- 🔀 **Git Integration** - Automatic branching, committing, merging, and pushing
- 🖼️ **Image Management** - Upload and insert images directly from your device
- 👁️ **Live Preview** - See how your posts will look before publishing
- 🔒 **Basic Authentication** - Simple username/password protection
- 🐳 **Docker Ready** - Pre-configured for Docker and Traefik deployment
- ⚡ **Automatic Deployment** - Triggers GitHub Actions when posts are published

## Architecture

```
blog-cms/
├── app/
│   ├── main.py              # Flask application
│   ├── git_manager.py       # Git operations handler
│   ├── post_manager.py      # Blog post CRUD operations
│   ├── templates/           # HTML templates
│   │   ├── login.html
│   │   ├── index.html       # Post listing
│   │   ├── editor.html      # WYSIWYG editor
│   │   └── preview.html     # Post preview
│   └── static/              # Static assets
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Traefik reverse proxy running
- Git repository for your blog
- SSH keys or git credentials configured

### Installation

1. **Clone or copy the CMS to your server:**

```bash
cd /path/to/your/home/server
git clone <this-repo> blog-cms
cd blog-cms
```

2. **Configure environment variables:**

```bash
cp .env.example .env
nano .env
```

Update the following values in `.env`:

**Docker Volume Paths:**
- `HOST_REPO_PATH` - Full path to your blog repository (e.g., `/home/user/blog-repo`)
- `HOST_SSH_PATH` - Path to your SSH keys (e.g., `/home/user/.ssh`)
- `HOST_GITCONFIG_PATH` - Path to your gitconfig (e.g., `/home/user/.gitconfig`)

**Container Configuration:**
- `CONTAINER_NAME` - Container name (defaults to `blog-cms`)
- `DOCKER_NETWORK` - Docker network name (defaults to `lan`)

**CMS Authentication:**
- `CMS_USERNAME` - Your admin username
- `CMS_PASSWORD` - Secure password for CMS access

**Security:**
- `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

**Git Configuration:**
- `GIT_AUTHOR_NAME` - Git author name for commits
- `GIT_AUTHOR_EMAIL` - Git author email for commits

**Traefik:**
- `TRAEFIK_DOMAIN` - Your CMS subdomain (e.g., `cms.yourdomain.com`)
- `TRAEFIK_CERT_RESOLVER` - Certificate resolver (defaults to `letsencrypt`)

3. **Ensure Traefik network exists:**

```bash
docker network create traefik-network
```

4. **Build and start the CMS:**

```bash
docker-compose up -d
```

5. **Access the CMS:**

Navigate to `https://cms.yourdomain.com` and log in with your credentials.

## Usage

### Creating a New Post

1. Click "New Post" from the main dashboard
2. Fill in the title, slug (URL-friendly name), description, and publish date
3. Write your content using the WYSIWYG editor
4. Upload images directly from your device (mobile-friendly)
5. Preview your post to see how it will look
6. Click "Save" to commit the post to a new git branch

### Editing a Post

1. Click "Edit" on any post from the dashboard
2. Make your changes
3. Click "Save" to commit updates

### Publishing a Post

1. Click "Publish" on a saved post
2. Confirm the action
3. The CMS will:
   - Merge the post's branch to master
   - Push to remote repository
   - Trigger GitHub Actions for deployment

### Deleting a Post

1. Click "Delete" on any post
2. Confirm the action
3. The post directory will be removed

## Git Workflow

The CMS follows this git workflow:

1. **Create Post** → Creates branch `blog/post-slug`
2. **Save Changes** → Commits to the post's branch
3. **Publish Post** → Merges `blog/post-slug` to `master` and pushes

This ensures:
- Draft posts are isolated on feature branches
- Master branch only contains published content
- GitHub Actions automatically deploys published posts

## Mobile Usage

The CMS is fully mobile-responsive:

- **Touch-friendly interface** - Large tap targets and mobile-optimized layouts
- **Image capture** - Use your phone's camera to add photos directly
- **WYSIWYG editing** - Full editor functionality on mobile devices
- **Preview mode** - Check posts on mobile before publishing

## Security Considerations

⚠️ **Important Security Notes:**

1. **Change default credentials** - Update `CMS_USERNAME` and `CMS_PASSWORD` immediately
2. **Use HTTPS** - Traefik provides automatic SSL via Let's Encrypt
3. **Secure your secret key** - Generate a strong random `SECRET_KEY`
4. **Restrict access** - Consider adding IP whitelisting via Traefik middleware
5. **SSH keys** - Ensure your git SSH keys are read-only in the container
6. **Rate limiting** - Add Traefik rate limiting middleware for production

### Adding IP Whitelist (Optional)

Add to docker-compose.yml:

```yaml
labels:
  - "traefik.http.routers.blog-cms.middlewares=blog-cms-ipwhitelist"
  - "traefik.http.middlewares.blog-cms-ipwhitelist.ipwhitelist.sourcerange=YOUR.IP.ADDRESS/32"
```

## Traefik Configuration

The CMS is configured to work with Traefik reverse proxy. Ensure your Traefik setup includes:

1. **Network** - External network named `traefik-network`
2. **Entry points** - `websecure` for HTTPS traffic
3. **Certificate resolver** - Let's Encrypt for automatic SSL

### Example Traefik docker-compose.yml

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik.yml:/traefik.yml:ro
      - ./acme.json:/acme.json
    networks:
      - traefik-network

networks:
  traefik-network:
    external: true
```

## Troubleshooting

### CMS won't start

- Check logs: `docker-compose logs -f blog-cms`
- Ensure repository path is correct
- Verify git credentials are mounted properly

### Can't push to git repository

- Check SSH keys are mounted: `-v ~/.ssh:/root/.ssh:ro`
- Verify git config is present
- Test git access: `docker exec -it blog-cms git remote -v`

### Images not uploading

- Check repository is writable
- Verify images directory exists
- Check disk space: `df -h`

### Traefik routing issues

- Verify Traefik network exists: `docker network ls`
- Check Traefik logs for routing errors
- Ensure domain DNS points to your server

## Development

### Local Development (without Docker)

```bash
cd blog-cms

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export REPO_PATH=/path/to/your/blog/repo
export CMS_USERNAME=admin
export CMS_PASSWORD=dev
export SECRET_KEY=dev-secret
export DEBUG=True

# Run Flask development server
cd app
python main.py
```

Access at `http://localhost:5000`

### Testing

```bash
# Test git operations
docker exec -it blog-cms python -c "from git_manager import GitManager; gm = GitManager('/repo'); print(gm.get_current_branch())"

# Test post listing
docker exec -it blog-cms python -c "from post_manager import PostManager; pm = PostManager('/repo/src/articles'); print(len(pm.list_posts()))"
```

## Customization

### Styling

The CMS uses Bootstrap 5. To customize:

1. Add custom CSS to `app/static/css/custom.css`
2. Update templates to include custom styles

### Adding Features

The modular architecture makes it easy to extend:

- **app/main.py** - Add new API endpoints
- **app/git_manager.py** - Extend git operations
- **app/post_manager.py** - Add post management features
- **app/templates/** - Customize UI

## Backup and Restore

Since the CMS works directly with your git repository:

- **Posts are version controlled** - Full history in git
- **Images are in the repo** - Backed up with your code
- **No database needed** - Everything is files

To backup:
```bash
cd /path/to/blog/repo
git push origin --all
```

## License

This CMS is designed for personal use with your blog. Modify freely for your needs.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Docker and Traefik logs
3. Ensure git configuration is correct

## Credits

Built with:
- Flask - Web framework
- Quill - WYSIWYG editor
- GitPython - Git integration
- Bootstrap 5 - UI framework
- Traefik - Reverse proxy
