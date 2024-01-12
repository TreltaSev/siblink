# pyright: reportUndefinedVariable=false
from typer import Option, Typer, Context
from typing import Union
from typing_extensions import Annotated


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def run(
  ctx: Context,
  source: Annotated[str, Option(help="Path to directory containing a main.py file or a directory which contains a main.py file.")] = "."
  ):
  """
  Creates and runs a python command, executes it while making sure to link all required packages and scripts by using a specific
  python environment and specific pip package.
  """
  console.info("[run] No Logic")
  return