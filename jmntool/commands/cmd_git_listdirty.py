from jmntool.cli import pass_environment
import click

import os
from git import Repo, InvalidGitRepositoryError

def get_git_urls(path):
    repo_names = []
    for root in next(os.walk('.'))[1]:
        try:
            repo = Repo(root)
            if repo.is_dirty():
                remote = repo.remotes.origin
                url = remote.url
                repo_name = url.split("/")[-1]
                if repo_name.endswith('.git'):
                    repo_name = repo_name[:-4]
                repo_names.append(repo_name)
        except InvalidGitRepositoryError:
            continue
        except:
            continue
    return repo_names

@click.command("listrepos", short_help="List all a repos.")
@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx, path):
    """Initializes a repository."""
    if path is None:
        path = ctx.home
    ctx.log(f"Listing repositories in {click.format_filename(path)}")
    urls = get_git_urls(path)
    for url in urls:
        ctx.log(f"{url}")