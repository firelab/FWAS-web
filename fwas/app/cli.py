import click
import click_log
from flask.cli import FlaskGroup

from . import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
@click_log.simple_verbosity_option()
def cli():
    """Management script for the fwas."""
