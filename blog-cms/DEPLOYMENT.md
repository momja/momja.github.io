# Blog CMS Deployment Guide

This guide walks you through deploying the Blog CMS on your home server with Traefik.

## Prerequisites Checklist

Before deploying, ensure you have:

- [ ] Docker installed on your server
- [ ] Docker Compose installed
- [ ] Traefik reverse proxy running
- [ ] Domain name pointing to your server
- [ ] SSH access to your server
- [ ] Git repository cloned on your server
- [ ] SSH keys configured for GitHub

## Step-by-Step Deployment

### 1. Prepare Your Server

```bash
# SSH into your server
ssh user@your-server.com

# Navigate to your docker projects directory
cd ~/docker-apps  # or wherever you keep Docker projects

# Clone/copy the CMS
git clone <repo-url> blog-cms
cd blog-cms
```

### 2. Configure Git Access

The CMS needs access to your blog repository to commit and push changes.

**Option A: Using SSH Keys (Recommended)**

```bash
# Ensure your SSH keys exist
ls -la ~/.ssh/id_rsa

# Test GitHub access
ssh -T git@github.com

# The docker-compose.yml will mount these automatically
```

**Option B: Using Git Credentials**

```bash
# Configure git credentials
git config --global user.name "Blog CMS"
git config --global user.email "cms@yourdomain.com"

# Store credentials (if using HTTPS)
git config --global credential.helper store
```

### 3. Clone Your Blog Repository

```bash
# Clone your blog repo to a location accessible by Docker
cd ~/repositories
git clone git@github.com:yourusername/yourblog.git

# Note the full path
pwd  # e.g., /home/user/repositories/yourblog
```

### 4. Configure the CMS

```bash
cd ~/docker-apps/blog-cms

# Copy environment file
cp .env.example .env

# Generate a secure secret key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Edit .env file
nano .env
```

Update these values in `.env`:

```bash
<<<<<<< Updated upstream
# ===== Docker Volume Paths =====
# Path to your blog repository on the host (from step 3)
HOST_REPO_PATH=/home/user/repositories/yourblog

# Path to SSH keys on host machine (for git push)
HOST_SSH_PATH=/home/user/.ssh

# Path to git config on host machine
HOST_GITCONFIG_PATH=/home/user/.gitconfig

# ===== Container Configuration =====
# Container name (optional, defaults to blog-cms)
CONTAINER_NAME=blog-cms

# Docker network name (should match your Traefik network)
DOCKER_NETWORK=traefik-network

# ===== Repository Configuration =====
# Internal repository path (inside container, don't change)
REPO_PATH=/repo

# ===== CMS Authentication =====
CMS_USERNAME=admin
CMS_PASSWORD=your_secure_password_here

# ===== Flask Secret Key =====
# Use the secret key generated above
SECRET_KEY=your_generated_secret_key_here

# ===== Git Configuration =====
=======
# Repository path (from step 3)
REPO_PATH=/home/user/repositories/yourblog

# CMS credentials
CMS_USERNAME=admin
CMS_PASSWORD=your_secure_password_here

# Secret key (from above)
SECRET_KEY=your_generated_secret_key_here

# Git configuration
>>>>>>> Stashed changes
GIT_AUTHOR_NAME=Blog CMS
GIT_AUTHOR_EMAIL=cms@yourdomain.com
GIT_COMMITTER_NAME=Blog CMS
GIT_COMMITTER_EMAIL=cms@yourdomain.com

<<<<<<< Updated upstream
# ===== Traefik Configuration =====
# Your CMS domain
TRAEFIK_DOMAIN=cms.yourdomain.com

# TLS cert resolver (defaults to letsencrypt)
TRAEFIK_CERT_RESOLVER=letsencrypt
```

**Important:** All configuration is now done via the `.env` file. You no longer need to edit `docker-compose.yml` manually.

### 5. Create Traefik Network
=======
# Your domain
TRAEFIK_DOMAIN=cms.yourdomain.com
```

### 5. Update docker-compose.yml

Edit `docker-compose.yml`:

```bash
nano docker-compose.yml
```

Update the volumes section with your actual paths:

```yaml
volumes:
  # Update this to your blog repository path
  - /home/user/repositories/yourblog:/repo

  # Mount SSH keys (for git push)
  - ~/.ssh:/root/.ssh:ro

  # Mount git config
  - ~/.gitconfig:/root/.gitconfig:ro
```

Update the Traefik labels with your domain:

```yaml
labels:
  - "traefik.http.routers.blog-cms.rule=Host(`cms.yourdomain.com`)"
  # ... other labels
```

### 6. Create Traefik Network
>>>>>>> Stashed changes

```bash
# Create the network if it doesn't exist
docker network create traefik-network

# Verify it exists
docker network ls | grep traefik
```

<<<<<<< Updated upstream
### 6. Configure DNS
=======
### 7. Configure DNS
>>>>>>> Stashed changes

Point your subdomain to your server:

```
Type: A
Name: cms
Value: YOUR_SERVER_IP
TTL: 3600
```

Wait for DNS propagation (check with `dig cms.yourdomain.com`).

<<<<<<< Updated upstream
### 7. Build and Start the CMS
=======
### 8. Build and Start the CMS
>>>>>>> Stashed changes

```bash
# Build the Docker image
docker-compose build

# Start the service
docker-compose up -d

# Check logs
docker-compose logs -f blog-cms
```

<<<<<<< Updated upstream
### 8. Verify Deployment
=======
### 9. Verify Deployment
>>>>>>> Stashed changes

```bash
# Check container status
docker ps | grep blog-cms

# Check logs for errors
docker-compose logs blog-cms

# Test git access
docker exec -it blog-cms git --version
docker exec -it blog-cms ssh -T git@github.com

# Verify repository is accessible
docker exec -it blog-cms ls -la /repo
```

<<<<<<< Updated upstream
### 9. Access the CMS
=======
### 10. Access the CMS
>>>>>>> Stashed changes

1. Open your browser to `https://cms.yourdomain.com`
2. Log in with your credentials from `.env`
3. Verify you can see your existing posts

## Post-Deployment Configuration

### Test Git Operations

1. Create a test post in the CMS
2. Check that a branch was created:
   ```bash
   docker exec -it blog-cms git -C /repo branch
   ```
3. Try publishing the post
4. Verify it was pushed to GitHub

### Set Up Automatic Updates (Optional)

Create a systemd service for automatic updates:

```bash
sudo nano /etc/systemd/system/blog-cms-update.service
```

```ini
[Unit]
Description=Blog CMS Update
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
WorkingDirectory=/home/user/docker-apps/blog-cms
ExecStart=/usr/bin/docker-compose pull
ExecStart=/usr/bin/docker-compose up -d

[Install]
WantedBy=multi-user.target
```

### Add Security Hardening

1. **IP Whitelist** - Restrict access to your IP:

```yaml
labels:
  - "traefik.http.routers.blog-cms.middlewares=blog-cms-ipwhitelist"
  - "traefik.http.middlewares.blog-cms-ipwhitelist.ipwhitelist.sourcerange=YOUR_HOME_IP/32"
```

2. **Rate Limiting** - Prevent brute force:

```yaml
labels:
  - "traefik.http.routers.blog-cms.middlewares=blog-cms-ratelimit"
  - "traefik.http.middlewares.blog-cms-ratelimit.ratelimit.average=100"
  - "traefik.http.middlewares.blog-cms-ratelimit.ratelimit.burst=50"
```

3. **HTTPS Only** - Force secure connections (already configured)

## Backup Strategy

The CMS doesn't need backups since all data is in your git repository:

1. **Posts** - Committed and pushed to GitHub
2. **Images** - Stored in repository's `images/` directory
3. **Configuration** - Keep `.env` backed up separately

Recommended backup command:

```bash
# Backup .env file
cp ~/docker-apps/blog-cms/.env ~/backups/blog-cms-env-$(date +%Y%m%d).backup
```

## Updating the CMS

To update the CMS to a new version:

```bash
cd ~/docker-apps/blog-cms

# Pull latest changes (if tracking a git repo)
git pull

# Rebuild
docker-compose build

# Restart with new image
docker-compose up -d

# Check logs
docker-compose logs -f
```

## Troubleshooting

### Can't access CMS at domain

1. Check DNS: `dig cms.yourdomain.com`
2. Check Traefik: `docker logs traefik`
3. Verify Traefik sees the service: `docker exec traefik traefik healthcheck`

### Git push fails

1. Check SSH key permissions:
   ```bash
   docker exec -it blog-cms ls -la /root/.ssh
   ```
2. Test GitHub access:
   ```bash
   docker exec -it blog-cms ssh -T git@github.com
   ```
3. Check git configuration:
   ```bash
   docker exec -it blog-cms git config --list
   ```

### Container won't start

1. Check logs: `docker-compose logs blog-cms`
2. Verify paths in docker-compose.yml
3. Ensure repository path is correct and accessible
4. Check permissions on mounted volumes

### Mobile upload not working

1. Ensure HTTPS is working (required for camera access)
2. Check browser permissions for camera
3. Verify images directory is writable

## Monitoring

Set up basic monitoring:

```bash
# Add to crontab for daily health checks
crontab -e

# Add this line:
0 9 * * * docker ps | grep blog-cms || echo "Blog CMS is down!" | mail -s "CMS Alert" your@email.com
```

Or use a monitoring service like Uptime Robot to ping `https://cms.yourdomain.com/`.

## Uninstalling

To completely remove the CMS:

```bash
cd ~/docker-apps/blog-cms

# Stop and remove container
docker-compose down

# Remove images
docker rmi blog-cms_blog-cms

# Remove files
cd ..
rm -rf blog-cms

# Your blog repository and git history remain intact
```

## Support Checklist

If something goes wrong, gather this information:

- [ ] Docker version: `docker --version`
- [ ] Docker Compose version: `docker-compose --version`
- [ ] Container logs: `docker-compose logs blog-cms > cms-logs.txt`
- [ ] Traefik logs: `docker logs traefik > traefik-logs.txt`
- [ ] Network configuration: `docker network inspect traefik-network`
- [ ] Container status: `docker ps -a | grep blog-cms`
- [ ] Git access test output
- [ ] Your domain and DNS configuration

## Next Steps

After successful deployment:

1. ✅ Test creating a post
2. ✅ Test image uploads
3. ✅ Test publishing workflow
4. ✅ Verify GitHub Actions triggered
5. ✅ Check live blog updated
6. ✅ Test mobile access
7. ✅ Set up monitoring
8. ✅ Document your customizations

Happy blogging! 🎉
