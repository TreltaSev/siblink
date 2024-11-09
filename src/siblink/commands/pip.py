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

    if Config.os == "win32":
      out.append(f"set PYTHONPATH=%PYTHONPATH%;{';'.join(scaffold.paths)}")
    else:
      out.append(f"export PYTHONPATH=\"$PYTHONPATH:{':'.join(scaffold.paths)}\"")

  if args[0] == "dump":

    try:
      _file = args[1]
    except IndexError:
      _file = "requirements.txt"

    con_start(f"Dumping to {colors.vibrant_violet}{_file}")
    out.append(f"{scaffold.pip} freeze > {_file}")
    os.system(command=' & '.join(out))
    quit()

  out.append(f"{scaffold.pip} {' '.join(args)}")

  if Config.os == "win32":
    command = ' & '.join(out)
  else:
    command = ' ; '.join(out)

  con_done(f"Command Running, {colors.vibrant_violet}{command}", show=True)

  os.system(command=command)
  return
