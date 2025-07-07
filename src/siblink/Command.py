from typing import List, Union, Literal
from siblink import Config
from pyucc import console
import pathlib


class RunScaffold:

  """
  Object used to create, mutate, and save the run command that makes siblink work.
  an object is used for easier representation. Requires :method:`Config.gather_predetermined`
  to be ran before.
  """

  def __init__(self, location: str | None, prioritize_script: bool = False, args: list = []):

    self.location = location
    self.prioritize_script = prioritize_script
    self.args = args

    if self.logic is "script":
      return

    self.paths: List[str] = []
    self.python: str = ""

    self.__get_script_location__()
    self.__gather_python__()
    self.__gather_pip__()

    self.__add_path__(Config.root)
    self.__add_path__(self.__subtract_commons__(location, pathlib.Path(".")))

  @property
  def logic(self) -> Literal["script", "python"]:
    if (not self.location_exists and self.is_script) or (self.location_exists and self.is_script and self.prioritize_script):
      return "script"
    return "python"

  def generate(self) -> str:
    """
    If the present logic is "script", this method will return the script command listed within siblink.config.json,
    if the present logic is "python", this method will return a command that sets the environment label and runs a python-esc.

    :return: str: Run command
    """
    if self.logic is "script":
      return self.get_script()
    if Config.os == "win32":
      return f"set PYTHONPATH=%PYTHONPATH%;{';'.join(self.paths)} & {self.python} -B {self.location} {' '.join(self.args)}"
    return f"export PYTHONPATH=\"$PYTHONPATH:{':'.join(self.paths)}\" && {self.python} -B {self.location} {' '.join(self.args)}"

  def get_script(self) -> None:

    # Check if config has scripts key
    if not hasattr(Config, "scripts"):
      raise NotImplementedError(f"No script key found in config.")

    if hasattr(Config.scripts, self.location):
      command = getattr(Config.scripts, self.location)

    return command

  @property
  def is_script(self) -> bool:
    """
    Checks if :arg:`self.location` is a registered script name

    :return: bool: True/False
    """
    try:
      return hasattr(Config.scripts, self.location)
    except Exception:
      return False

  @property
  def location_exists(self) -> bool:
    """
    returns bool representing if self.location is a valid file or directory
    """
    try:
      return pathlib.Path(self.location).exists()
    except Exception:
      return False

  def __gather_python__(self) -> None:
    """
    Gets location of python command
    """
    self.python = Config.python_exe.absolute() if Config.venv.exists() else "python"

  def __gather_pip__(self) -> None:
    """
    Gets location of pip command
    """
    self.pip = Config.pip_exe.absolute() if Config.venv.exists() else "pip"

  def __get_script_location__(self) -> None:
    """
    Attempts to get the path for the script the user is running, whether its a package
    or a file. Contains error handling.
    """

    if not self.location:
      return
    location: pathlib.Path = pathlib.Path(str(self.location))

    if not location.exists():
      console.warn(f"\"{location}\" is not a valid path, please check if you've typed it correctly. If \"{self.location}\" is the name of a registered script, please add the -s or --script flag to this command.")
      quit()

    if location.is_file():
      self.location = Config.__absolute__(self.location)

    if location.is_dir():
      normal_file = next(location.glob("main.py"), None)
      magic_file = next(location.glob("__main__.py"), None)
      if magic_file is not None:
        self.location = str(Config.__absolute__(magic_file))
      elif normal_file is not None:
        self.location = str(Config.__absolute__(normal_file))
      else:
        console.error(f"Inputted directory \"{self.location}\" does not contain a main.py or __main__.py file")
        quit()

  def __add_path__(self, path: Union[List[str], str, pathlib.Path]):
    """
    Takes in the inputted `path` variable then appends it to `self.paths`, all after
    checking if the path is valid or if its a string of multiple paths.

    :arg Path: Union[List[str], str, pathlib.Path]: String representation of path
    """

    # Turn pathlib into string
    if isinstance(path, pathlib.Path):
      path = str(path.absolute())

    # Handle Path if string
    if isinstance(path, str):
      for child_path in path.split(";"):
        self.__validate_and_append__(child_path)

    # Handle Path if list
    if isinstance(path, list):
      for child_path in path:
        self.__validate_and_append__(child_path)

  def __validate_and_append__(self, path: str):
    """
    Checks the inputted path see if it exists, if it exists, appends to `self.paths`

    :arg path: str: String representation of path
    """
    if not Config.__exists__(path):
      console.warn(f"[RunScaffold] path not valid/does not exist \"{path}\"")
      return
    self.paths.append(Config.__absolute__(path))

  @classmethod
  def __subtract_commons__(cls, path, compare):
    """
    Subtracts the common directories between path and compare, the results
    will be turned into a list containing absolute paths.
    :arg path: The path with branching
    :arg compare: the path to compare against.
    """
    if not path:
      path = pathlib.Path(".").absolute()
    path = Config.__absolute__(path)
    compare = Config.__absolute__(compare)

    if not Config.__exists__(path) or not Config.__exists__(compare):
      console.warn(f"[subtract commons] Config paths one or more not exist: {path}, {compare}")
      return []

    # Split Paths
    path_split = Config.__absolute__(path).split("\\")
    compare_split = Config.__absolute__(compare).split("\\")

    # Gather Common
    common_zip = []
    for full, base in zip(path_split, compare_split):
      if not full == base:
        break
      common_zip.append(full)

    # Subtract Common
    subtracted = path_split[len(common_zip):]

    # Get Results
    results = []
    for i in range(len(subtracted)):
      result_path = "\\".join(common_zip + subtracted[:i+1])
      if pathlib.Path(result_path).is_dir():
        results.append(Config.__absolute__(result_path))

    return results
