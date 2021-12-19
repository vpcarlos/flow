import typer

from enum import Enum
from flow.models.flow import Flow
from flow.commands.start.start import app as start_app


app = typer.Typer()

app.add_typer(start_app, name='start')


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
