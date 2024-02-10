import os
import click
import pathlib
from pyucc import console
from siblink import Config


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
  location: pathlib.Path = pathlib.Path(location)

  if not location.exists():
    console.warn(f"\"{location}\" is not a valid path, please check if you've typed it correctly. If \"{location}\" is the name of a registered script, please add the -s or --script flag to this command.")
    return

  gathered_python: str = Config.python_exe.absolute() if Config.venv.exists() else "python"
  command = f"set PYTHONPATH=%PYTHONPATH%;{Config.root.absolute()} & {gathered_python} -B"

  # Append location of file
  if location.is_file():
    command = ' '.join(command, str(location.absolute()))

  # Check if Directory search for main.py file in dir
  if location.is_dir():
    normal_file = next(location.glob("**/main.py"), None)
    magic_file = next(location.glob("**/__main__.py"), None)

    if magic_file is not None:
      command = ' '.join([command, str(location.absolute())])
    if normal_file is not None:
      command = ' '.join([command, str(normal_file)])
    else:
      console.error(f"Inputted directory does not contain a main.py or __main__.py file, If \"{location}\" is the name of a registered script, please add the -s or --script flag to this command.")
      return

  # Add Extra Arguments to Command if present
  if args:
    command = ' '.join([command, ' '.join(args)])

  # Notify
  console.info(f"[run] Running Command: \"{command}\"")

  # Run Command
  os.system(command=command)
  return
