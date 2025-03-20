#!/usr/bin/env python3

import os
import sys

import click


CONTEXT_SETTINGS = dict(auto_envvar_prefix="JMNTOOL")


class Environment:
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class JmntoolCLI(click.Group):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"jmntool.commands.cmd_{name}", None, None, ["cli"])
        except ImportError:
            print(f"ImportError: {name}")
            return
        return mod.cli


@click.command(cls=JmntoolCLI, context_settings=CONTEXT_SETTINGS)
@click.option(
    "--home",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help="Changes the folder to operate on.",
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def cli(ctx, verbose, home):
    """A Jmntool command line interface."""
    ctx.verbose = verbose
    if home is not None:
        ctx.home = home
