import click
import click_log

from fwas.worker import run_worker
from fwas.tasks import clear_scheduled_jobs


@click.group()
@click_log.simple_verbosity_option()
def cli():
    """Management script for the fwas."""


@cli.command()
def runworker():
    run_worker()


@cli.command()
def clear_jobs():
    clear_scheduled_jobs()
