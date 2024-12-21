import typer

app = typer.Typer()


@app.callback()
def callback():
    """
    Synchronizes with the public rule repositories
    """
    print("syncing :)")


@app.command(name="all")
def sync_all():
    sync_sigmahq()


@app.command(name="sigmahq")
def sync_hq():
    sync_sigmahq()


def sync_sigmahq():
    pass
