import sys
import os
import logging
import shutil
import distutils
import time
from datetime import datetime

import click
import click_log
from fabric import Connection, Config
from invoke import run

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def pack(tarname):
    """Create a tarball of the FWAS source."""
    logger.info(f"Creating tarball of FWAS..")
    tar_files = ' '.join(['*'])
    run(f'rm -f {tarname}')
    run(f"tar -czvf {tarname} --exclude='*.tar.gz' --exclude='fabfile.py' {tar_files}", hide=True)
    logger.info(f"Successfully created tarball")


def upload_and_unpack(connection, tarname):
    """Upload a tarball to a remote host.

    Args:
        connection (fabric.Connection): Fabric connection for the remote host
        tarname (str): Name of the tarball to upload
    """
    logger.info(f"Copying {tarname} to on {connection.host}")
    connection.put(tarname, '/tmp')
    connection.run(f'tar -C /tmp -xzvf /tmp/{tarname}', hide=True)
    logger.info(f"Successfully coped and exactracted FWAS source.")


@click.command()
@click.argument("parts", type=click.Choice(["all", "app", "config", "data", "apache", "supervisor"]))
@click.option('-t', '--target', default=None)
@click.option('-d', '--destination', default='/tmp/srv')
@click.option('-h', '--host' )
@click_log.simple_verbosity_option()
def deploy(parts, target, destination, host):
    """Deploy FWAS to a remote destination.

    Args:
        parts (str): What to deploy.
        target (str): What tarball to upload. If empty, a tarball will be created.

    """
    logger.info(f"{sys.version} {sys.executable}")
    config = Config(overrides={'connect_kwargs': {'key_filename': 'WindNinjaMobile.pem'}})
    connection = Connection(host, config=config)

    source = '/tmp/fwas'

    if target is None:
        tag = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        target = f'windninja_server_{tag}.tar.gz'
        pack(target)

    # prepare a tarball of the source code and copy it to the host
    logger.info(f"Deploying fwas {host}")
    upload_and_unpack(connection, target)

    connection.sudo(f'chown -R ubuntu:ubuntu {destination}')

    # TODO (lmalott): fill out with proper task definitions
    # (1) Configure server groups (web, scheduler, and worker)
    # (2) For each group install the app requirements.
    # (3) For the web server, configure nginx and start it.
    # (4) For the web server, configure supervisor to start nginx
    # (5) For the web server, start the flask app via gunicorn
    # (6) For the worker, configure supervisor to run `pipenv run fwas runworker`
    # (7) For the schduler, configure supervisor to run `pipenv run fwas scheduler`

    reload_services(connection)

    logger.info("complete!")


if __name__=="__main__":
    deploy()
