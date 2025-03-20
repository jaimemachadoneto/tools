from jmntool.cli import pass_environment
import click
from typing import List
import os
from git import Repo, InvalidGitRepositoryError

def get_git_urls(ctx, path, doPull) -> List[str]:
    repo_names = []
    folders = []
    for root in next(os.walk('.'))[1]:
        folders.append(root)
    folders.sort()
    for root in folders:
        try:
            repo = Repo(root)
            default_branch = 'main' if 'main' in repo.branches else 'master'
            remote = repo.remotes.origin
            url = remote.url            
            repo_name = url.split("/")[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            
            if repo.is_dirty():
                repo_names.append(repo_name)
            else:
                commits_behind = repo.iter_commits(f'origin/{default_branch}..{default_branch}')
                if sum(1 for c in commits_behind):
                    ctx.log(f"{repo_name} has commits that have not been pushed.")
                    continue                
                # Check if the active branch is the default branch
                if repo.active_branch.name != default_branch:
                    ctx.log(f"{repo_name} is not on the default branch. Moving to {default_branch}.")
                    # If not, checkout the default branch
                    repo.git.checkout(default_branch)     
                if doPull:
                    ctx.log(f"Pulling {repo_name}!")                    
                    repo.git.pull()           
        except InvalidGitRepositoryError:
            continue
        except Exception as e:
            print("jaime  Exception: " + str(e))
            continue
    return repo_names

@click.command("git_gomain", short_help="Move all repos on folder to main if possible.")
@click.argument("path", required=False, type=click.Path(resolve_path=True))
@click.option("-p", is_flag=True, show_default=True, default=False, help="Also do a pull on repos that are not dirty.")
@pass_environment
def cli(ctx, path, p):
    """Initializes a repository."""
    if path is None:
        path = ctx.home
    ctx.log(f"Listing repositories in {click.format_filename(path)}")
    urls = get_git_urls(ctx, path, p)
    ctx.log(f"Found {len(urls)} dirty repos.")
    for url in urls:
        ctx.log(f"{url}")