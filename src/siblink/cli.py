import os
import typer
from pyucc import console
from pathlib import Path
from typer import Option
from typing_extensions import Annotated
from . import Config, __git__

app = typer.Typer()


def siblink_index(contents: str) -> int:
  for index, key in enumerate(contents.split("\n")):
    if key.startswith("siblink"):
      return index
  return len(contents.split("\n")) - 1


def refactored_contents(contents: str) -> str:
  out: list = contents.split("\n")
  out[siblink_index(contents)] = f"siblink @ {__git__}"
  return "\n".join(out)


def pd_logic(out: str = "./requirements.txt"):
  console.info("[__pip_dumping__]")

  if Config.gather_predetermined() is 0:
    console.error("This command needs './venv' to be present")
    quit()

  os.system(f"{Config.pip_exe.absolute()} freeze > {out}")
  Path(out).write_text(refactored_contents(Path(out).read_text()))


@app.command()
def pip_dump(
    out: Annotated[str, Option(help="Path to where the the packages will be dumped")] = "./requirements.txt"
):
  """
  Dumps all pypi packages into a requirements.txt file, or whatever --out is set to.
  """
  console.info("[pip_dump]")
  pd_logic(out)
  return


@app.command()
def pd(
    out: Annotated[str, Option(help="Path to where the the packages will be dumped")] = "./requirements.txt"
):
  """
  Alias to `siblink pip-dump`
  """
  console.info("[pd]")
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
