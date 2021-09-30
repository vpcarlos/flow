import typer
import os

from flow.models.flow import Feature
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

    r = os.system('ls')

    print(r)
