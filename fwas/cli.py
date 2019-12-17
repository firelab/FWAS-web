import click
import click_log
from flask.cli import FlaskGroup, with_appcontext

from . import create_app
from .worker import run_worker


@click.group(cls=FlaskGroup, create_app=create_app)
@click_log.simple_verbosity_option()
def cli():
    """Management script for the fwas."""


@cli.command()
@with_appcontext
def runworker():
    run_worker()
