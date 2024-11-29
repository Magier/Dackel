from pathlib import Path
from typing import Annotated
import typer
from dotenv import load_dotenv
import yaml

from endpoints.cast import CastAiApi
from rule import Rule

load_dotenv()

app = typer.Typer()


def load_rules() -> list[Rule]:
    src_dir = Path("rules")
    rules = []
    for r in src_dir.glob("**/*.yaml"):
        with open(r) as f:
            data = yaml.safe_load(f)
        rules.append(Rule(**data))
    return rules


@app.command()
def main(
    api_server: Annotated[str, typer.Argument(envvar="CAST_API")],
    api_token: Annotated[str, typer.Argument(envvar="CAST_TOKEN")],
):
    rules = load_rules()
    cast = CastAiApi(server=api_server, token=api_token)
    cast.upsert_rules(rules)
    new_rules = cast.get_rules()
    print(f"Got {len(new_rules)} rules!")


if __name__ == "__main__":
    app()
