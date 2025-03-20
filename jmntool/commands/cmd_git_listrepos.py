from jmntool.cli import pass_environment
import click

import os
from git import Repo, InvalidGitRepositoryError

def get_git_urls(path):
    urls = []
    for root in next(os.walk('.'))[1]:
        try:
            repo = Repo(root)
            remote = repo.remotes.origin
            url = remote.url
            urls.append(url)
        except InvalidGitRepositoryError:
            continue
        except:
            continue
    return urls

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