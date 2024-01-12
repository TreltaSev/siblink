import os
import typer
from pyucc import console
from pathlib import Path
from typer import Option
from typing_extensions import Annotated

app = typer.Typer()

def pd_logic(out: str = "./requirements.txt"):
  console.info("[__pip_dumping__] No Logic")

@app.command()
def pip_dump(
  out: Annotated[str, Option(help="Path to where the the packages will be dumped")] = "./requirements.txt"
  ):
  """
  Dumps all pypi packages into a requirements.txt file, or whatever --out is set to.
  """
  console.info("[pip_dump] No Logic")
  pd_logic(out)
  return

@app.command()
def pd(
  out: Annotated[str, Option(help="Path to where the the packages will be dumped")] = "./requirements.txt"
  ):
  """
  Alias to `siblink pip-dump`
  """
  console.info("[pd] No Logic")
  pd_logic(out)
  return


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
  if ctx.invoked_subcommand is None:
    return


def main():
  commands_directory = Path(__file__).parent / "commands"
  commands = [child for child in commands_directory.iterdir() if str(child).endswith(".py")]
  for command_path in commands:
    exec(Path(command_path).read_text())
  app()


if __name__ == "__main__":
  main()
