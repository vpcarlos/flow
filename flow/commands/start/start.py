import typer
from enum import Enum
from flow.models.flow import Release, Feature

app = typer.Typer()

class VersionType(str, Enum):
    major = 'major'
    minor = 'minor'
    patch = 'patch'


@app.command()
def feature(name: str):
    """Start a new flow feature branch. """
    Feature.git_flow('start', name)


@app.command()
def release(version_type: VersionType):
    """Start a new flow release branch. """
    next_v = Release.build_next(version_type.value)
    Release.git_flow('start', next_v)
