"""Git operations manager for blog CMS."""
import os
from git import Repo
from datetime import datetime


class GitManager:
    """Manages git operations for blog posts."""

    def __init__(self, repo_path):
        """Initialize git manager with repository path."""
        self.repo_path = repo_path
        self.repo = Repo(repo_path)

    def create_branch(self, branch_name):
        """Create and checkout a new branch."""
        try:
            # Fetch latest from origin
            origin = self.repo.remotes.origin
            origin.fetch()

            # Create new branch from master
            current = self.repo.head.reference
            master = self.repo.heads.master

            # Create new branch
            new_branch = self.repo.create_head(branch_name, master)
            new_branch.checkout()

            return True, f"Created and checked out branch: {branch_name}"
        except Exception as e:
            return False, str(e)

    def commit_changes(self, file_paths, commit_message):
        """Commit changes to specified files."""
        try:
            # Add files to staging
            self.repo.index.add(file_paths)

            # Commit
            commit = self.repo.index.commit(commit_message)

            return True, f"Committed: {commit.hexsha[:7]}"
        except Exception as e:
            return False, str(e)

    def merge_to_master(self, branch_name):
        """Merge current branch to master."""
        try:
            # Checkout master
            master = self.repo.heads.master
            master.checkout()

            # Merge the branch
            branch = self.repo.heads[branch_name]
            self.repo.git.merge(branch.name)

            return True, f"Merged {branch_name} to master"
        except Exception as e:
            return False, str(e)

    def push_to_remote(self, branch_name='master'):
        """Push changes to remote repository."""
        try:
            origin = self.repo.remotes.origin
            origin.push(branch_name)

            return True, f"Pushed {branch_name} to remote"
        except Exception as e:
            return False, str(e)

    def get_current_branch(self):
        """Get current branch name."""
        return self.repo.active_branch.name

    def checkout_branch(self, branch_name):
        """Checkout an existing branch."""
        try:
            branch = self.repo.heads[branch_name]
            branch.checkout()
            return True, f"Checked out: {branch_name}"
        except Exception as e:
            return False, str(e)

    def list_branches(self):
        """List all branches."""
        return [head.name for head in self.repo.heads]

    def get_unpublished_branches(self):
        """Get branches that haven't been merged to master."""
        branches = []
        for branch in self.repo.heads:
            if branch.name != 'master' and branch.name.startswith('blog/'):
                branches.append(branch.name)
        return branches

    def delete_branch(self, branch_name, force=False):
        """Delete a local branch and optionally push deletion to remote."""
        try:
            # Make sure we're not on the branch we're trying to delete
            current_branch = self.get_current_branch()
            if current_branch == branch_name:
                # Checkout master first
                master = self.repo.heads.master
                master.checkout()

            # Delete local branch
            if branch_name in [head.name for head in self.repo.heads]:
                self.repo.delete_head(branch_name, force=force)

            # Try to delete remote branch (it's okay if it doesn't exist)
            try:
                origin = self.repo.remotes.origin
                origin.push(refspec=f":{branch_name}")
            except Exception as e:
                # Remote branch might not exist, that's okay
                pass

            return True, f"Deleted branch: {branch_name}"
        except Exception as e:
            return False, str(e)
