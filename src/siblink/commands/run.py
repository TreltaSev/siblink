import os
import click
import pathlib
from pyucc import console
from siblink import Config, Command


@click.command()
@click.argument("location")
@Config.click_forward
@Config.load_predetermined
@Config.load_config
def run(location: str):
  """
  Run python scripts and programs with this command by referencing a file or directory which contains a main.py file.

  location(str): Path of script or directory to run, if the inputted is a directory, a main.py file or __main__.py file is checked for within the said directory.
  """

  command = Command.RunScaffold(location).generate()

  # Notify
  console.info(f"[run] Running Command: \"{command}\"")

  # Run Command
  os.system(command=command)
  return
