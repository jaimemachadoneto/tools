from jmntool.cli import pass_environment
import click

import os
from git import Repo, InvalidGitRepositoryError

from git import GitCommandError

def clone_repos(ctx, repos_file, path):
    with open(repos_file, 'r') as file:
        repos = [line.strip() for line in file if line.strip()]
    for url in repos:
        repo_name = url.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(path, repo_name)
        try:
            Repo.clone_from(url, repo_path, recursive=True)
            ctx.log(f"Cloned {url} into {repo_path}")
        except GitCommandError as e:
            ctx.log(f"Failed to clone {url}: {str(e)}")
            continue
        
@click.command("listrepos", short_help="List all a repos.")
@click.argument("path", required=True, type=click.Path(resolve_path=True))
@click.argument("reposfile", required=True, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx, path, reposfile):
    print(path)
    print(reposfile)
    """Clone all repos within a file."""
    if path is None:
        path = ctx.home
    ctx.log(f"Listing repositories in {click.format_filename(path)}")
    urls = clone_repos(ctx, reposfile, path)
    for url in urls:
        ctx.log(f"{url}")