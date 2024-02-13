import os
import click
import pathlib
from pyucc import console
from siblink import Config, Command


@click.command()
@click.argument("location")
@click.argument("args", nargs=-1)
@Config.load_predetermined
def run(location: str, args):
  """
  Run python scripts and programs with this command by referencing a file or directory which contains a main.py file.

  location(str): Path of script or directory to run, if the inputted is a directory, a main.py file or __main__.py file is checked for within the said directory.

  args(any): Any value past the location string will be added to the end of the compiled command. Limited to anything that doesn't contain ";" or starts with "-" or "--"
  """

  command = Command.RunScaffold(location).generate()

  # Add Extra Arguments to Command if present
  if args:
    command = ' '.join([command, ' '.join(args)])

  # Notify
  console.info(f"[run] Running Command: \"{command}\"")

  # Run Command
  os.system(command=command)
  return
