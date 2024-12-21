from pathlib import Path
from typing import Annotated
import typer
import yaml

from endpoints.cast import CastAiApi
from rule import Rule


app = typer.Typer()


def load_rules() -> list[Rule]:
    src_dir = Path("rules")
    rules = []
    for r in src_dir.glob("**/*.yaml"):
        with open(r) as f:
            data = yaml.safe_load(f)
        rules.append(Rule(**data))
    return rules


@app.command(name="castai")
def upsert_castai(
    api_server: Annotated[str, typer.Argument(envvar="CAST_API")],
    api_token: Annotated[str, typer.Argument(envvar="CAST_TOKEN")],
):
    """
    Updates and/or inserts any new rules to the specified detection system.
    """
    rules = load_rules()
    cast = CastAiApi(server=api_server, token=api_token)
    cast.upsert_rules(rules)
    new_rules = cast.get_rules()
    print(f"Got {len(new_rules)} rules!")
