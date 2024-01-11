import os
import glob
import typer
import subprocess
from pathlib import Path
from pyucc import console
from . import Config, __git__
from typing import Optional, Union, List
from typing_extensions import Annotated


app = typer.Typer(pretty_exceptions_show_locals=False)


@Config.load_config
@app.command(name="run")
def run(run_path: str, args: List[str] = []):
  """
  Run python files or directories which contain a main.py file.
  """
  run_path: Path = Path(run_path)
  command = f"set PYTHONPATH=%PYTHONPATH%;{Config.root.absolute()} & {Config.python_exe.absolute()} -B "

  if run_path.is_file():
    command += str(run_path.absolute())

  if run_path.is_dir():
    main_file = glob.glob(str(run_path / "main.py"))
    if len(main_file) == 0:
      raise FileNotFoundError(
          f"No main.py file found in {run_path.absolute()}")
    command += main_file[0]

  command += f" {' '.join(args)}"

  console.info(f"Running Command: \"{command}\"")
  os.system(command)


@Config.load_config
@app.command(name="script")
def script(script_name: Annotated[Union[str, None], typer.Argument()], args: List[str] = []):
  """
  Run registered or unregistered scripts within the ./scripts directory, if the command is registered, the path is already defined within the Config file, if the script path is not located within the Config file,
  this command will attempt to find that file within a specified scripts directory, if `scripts` is undefined, it will default to "./scripts/" if all else fails, a error will be displayed on the screen.


  :arg script_name: `(Annotated[Union[str, None], typer.Argument, optional): _description_. Defaults to None.`


  :arg scripts: Parent directory of all the script files to be ran, this will most likely be used whenever the script_name you inputted isn't defined within the Config.json file`(Annotated[Optional[str], typer.Option, optional]): _description_. Defaults to None`
  """

  console.error("This command is currently not updated and is currently disabled.")
  return


def siblink_index(contents: str) -> int:
  for index, key in enumerate(contents.split("\n")):
    if key.startswith("siblink"):
      return index
  return len(contents.split("\n"))


def refactored_contents(contents: str) -> str:
  out: list = contents.split("\n")
  out[siblink_index(contents)] = f"siblink @ git+{__git__}"
  return "\n".join(out)


@Config.load_config
def __pip_dumping__(requirements_txt_path: Optional[str] = "./requirements.txt"):
  console.info(f"Dumping Modules to {requirements_txt_path}")
  command = f"{Config.pip_exe.absolute()} freeze > {requirements_txt_path}"
  os.system(command)

  # Not at all confusing :)
  Path(requirements_txt_path).write_text(refactored_contents(Path(requirements_txt_path).read_text()))


@app.command(name="pd")
def pd(requirements_txt_path: Optional[str] = "./requirements.txt"):
  """
  Shorthand for `siblink pip_dump`
  """
  __pip_dumping__(requirements_txt_path=requirements_txt_path)


@app.command(name="pip_dump")
def pip_dump(requirements_txt_path: Optional[str] = "./requirements.txt"):
  """
  Runs pip freeze > command
  """
  __pip_dumping__(requirements_txt_path=requirements_txt_path)


@Config.load_config
@app.command(name="install")
def install():
  """
  Installs the latest version of siblink into a python project's virtual environment as well as the global python environment
  """
  try:
    console.info("About to attempt Config.venv")
    print(Config.venv)
  except Exception as e:
    console.error(f"Failed ;(, {e}")
  return
  console.info(f"Installing siblink to global path")
  subprocess.run(f"pip install --upgrade --force-reinstall -I git+{__git__}".split(" "), capture_output=True)
  console.info(f"Installing siblink to {Config.venv.absolute()}...")
  subprocess.run(f"{Config.pip_exe.absolute()} install --upgrade --force-reinstall -I git+{__git__}".split(" "), capture_output=True)


def exper():
  print(":)")
  return True


@app.command(name="test")
def test():
  console.info("Testing")


def main():
  app()


if __name__ == "__main__":
  main()
