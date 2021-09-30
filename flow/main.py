import typer
from flow.commands import feature

app = typer.Typer()
app.add_typer(feature.app, name='feature', help='Flow feature',)


if __name__ == "__main__":
    typer.run(app)
