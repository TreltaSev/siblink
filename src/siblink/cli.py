import os
import typer
from pyucc import console
from pathlib import Path

app = typer.Typer()


@app.command()
def entry():
  print("...")


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
