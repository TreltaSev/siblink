import os
import click
import pathlib
from pyucc import console
from siblink import Config, Command


@click.command()
@click.argument("location")
@click.argument("args", nargs=-1)
@click.option("--ps", is_flag=True, show_default=True, default=False, help="Prioritize Registered Scripts")
@Config.click_forward
@Config.load_predetermined
@Config.load_config
def run(location: str, ps: bool, args: list):
  """
  Run python scripts and programs with this command by referencing a file or directory which contains a main.py file.

  location(str): Path of script or directory to run, 
  or a registered script within siblink.config.json, 
  if the inputted is a directory, a main.py file or __main__.py 
  file is checked for within the said directory.
  If the inputted is a registered script, the command listed in the config file will be ran instead.
  This command automatically prioritizes files/directories over registered scripts. If you want
  to run a script even though the name of the script is also the name of a file, you should consider
  using the --ps flag.
  """

  command = Command.RunScaffold(location, ps, args).generate()

  # Notify
  console.info(f"[run] Running Command: \"{command}\"")

  # Run Command
  os.system(command=command)
  return
