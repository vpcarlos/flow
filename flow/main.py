import typer

from enum import Enum
from flow.models.flow import Flow, Release, Feature

app = typer.Typer()
start = typer.Typer()

app.add_typer(start, name='start')


class VersionType(str, Enum):
    major = 'major'
    minor = 'minor'
    patch = 'patch'


@start.command()
def feature(name: str):
    """Start a new flow feature branch. """
    Feature.git_flow('start', name)


@start.command()
def release(version_type: VersionType):
    """Start a new flow release branch. """
    next_v = Release.build_next(version_type.value)
    Release.git_flow('start', next_v)


@app.command()
def publish():
    """Publish flow. """
    flow = Flow.factory()
    branch = flow.get_flow_branch()
    flow.git_flow('publish', branch)
    typer.launch(flow.get_new_pr_url())


@app.command()
def finish():
    """Finish flow. """
    flow = Flow.factory()
    branch = flow.get_flow_branch()
    flow.git_flow('finish', branch)


if __name__ == "__main__":
    app()
