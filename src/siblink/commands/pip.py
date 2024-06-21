import os
import click
from siblink.Command import RunScaffold
from pathlib import Path
from pyucc import console, colors, symbols
from siblink import Config


def con_start(*args, show: bool = True):
  if show:
    console.start(*args)


def con_done(*args, show: bool = True):
  if show:
    console.done(*args)


def con_info(*args, show: bool = True):
  if show:
    console.info(*args)


@click.command()
@click.option("--venv/--no-venv", default=True)
@click.option("--debug/--no-debug", default=True)
@click.argument("args", nargs=-1)
def pip(venv, debug, args):
  """
  Shorthand command for python's builtin pip command, with optional virtual environment automatic selection
  """

  con_start("Generating Scaffold", show=debug)
  Config.gather_predetermined()
  scaffold: RunScaffold = RunScaffold(None, False, [])

  con_done("Scaffold Generated", show=debug)
  out: list[str] = []

  if venv:
    con_info("Handling Venv Assignment", show=debug)
    out.append(f"set PYTHONPATH=%PYTHONPATH%;{';'.join(scaffold.paths)}")

  out.append(f"pip {' '.join(args)}")

  command = ' & '.join(out)

  con_done(f"Command Running, {colors.vibrant_violet}{command}", show=True)

  os.system(command=command)
  return
