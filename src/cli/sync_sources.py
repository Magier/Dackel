import typer
from rule_sources import sigmahq

app = typer.Typer()


@app.callback()
def callback():
    """
    Synchronizes with the public rule repositories
    """


@app.command(name="all")
def sync_all():
    sigmahq.sync()
