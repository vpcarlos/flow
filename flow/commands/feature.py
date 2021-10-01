import typer
import os
import subprocess

from flow.models.flow import Feature
from flow.models.shell import Shell as shell

import git

app = typer.Typer()


@app.command()
def start(branch: str):
    """
    Start a new flow feature branch
    """
    Feature.command('start', branch)


@app.command()
def publish():
    """
    Publish flow feature
    """

    Feature.command('publish')


@app.command()
def demo():
    res = Feature.get_flow_branch()
    
