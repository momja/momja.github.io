#!/bin/bash
set -e

# Mark the repository directory as safe for git operations
# This prevents "dubious ownership" errors when the repo is mounted from host
git config --global --add safe.directory /repo

# Configure git user if environment variables are set
if [ -n "$GIT_AUTHOR_NAME" ]; then
    git config --global user.name "$GIT_AUTHOR_NAME"
fi

if [ -n "$GIT_AUTHOR_EMAIL" ]; then
    git config --global user.email "$GIT_AUTHOR_EMAIL"
fi

# Execute the main command
exec "$@"
