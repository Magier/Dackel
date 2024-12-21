import typer
from dotenv import load_dotenv
from . import sync_sources
from . import upsert

load_dotenv()

app = typer.Typer()
app.add_typer(sync_sources.app, name="sync", invoke_without_command=True)
app.add_typer(upsert.app, name="upsert")
