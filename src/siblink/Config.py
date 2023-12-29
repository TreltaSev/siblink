import os
import json
import glob
import collections
from pathlib import Path
from pyucc import console, colors
from typing import Any, List, Union


class ScriptHandler:

  @classmethod
  def get(cls, script_name: str):
    """
    Method is used to get the path of a inputted script variable, this script variable could be a name or a direct or relative path
    to a script. Local scripts or script names should be saved in config.json within siblink and scripts.
    :arg script_name: str: The script to be converted
    """
    parent = Config.raw["siblink"]["scripts"].get("$parent", None)

    if not script_name in Config.raw["siblink"]["scripts"]:
      path: Path = Path(script_name)

      if not path.exists():
        console.error(f"\"{script_name}\" is not found within {colors.vibrant_violet}siblink.conf{colors.vibrant_red} under a script header nor is it a file...")
        quit()

      return path

    script_path_in_config: str = Config.raw["siblink"]["scripts"].get(script_name)
    if parent is not None:
      script_path_in_config = script_path_in_config.replace("$", parent, 1)

    script_path: Path = Path(script_path_in_config)

    if not script_path.exists():
      console.error(f"\"{script_name}\" contains invalid or not found {colors.vibrant_violet}path{colors.vibrant_yellow} {script_path.absolute()}")
      quit()

    return script_path


class Config:
  """
  Handle, Create, Read, and Generate Config Files
  used interchangeably between programs.
  """

  os_switch: str = 'Scripts' if os.name == "nt" else "bin"

  def __init__(self) -> None:
    if not hasattr(Config, "loaded"):
      setattr(Config, "ScriptHandler", ScriptHandler)
      Config.__get_raw__()

  @classmethod
  def deep_update(cls, to_update: Union[dict, collections.abc.Mapping], data: Union[dict, collections.abc.Mapping]) -> dict:
    """
    Recursive updating of dictionaries, used in the :method:`__get_raw__()` method.
    :arg to_update: Union[dict, collections.abc.Mapping]: The dictionary that will be updated
    :arg data: Union[dict, collections.abc.Mapping]: The dictionary that contains the data that will be implanted into :variable:`to_update`
    """
    for k, v in data.items():
      if isinstance(v, collections.abc.Mapping):
        to_update[k] = cls.deep_update(to_update.get(k, {}), v)
      else:
        to_update[k] = v
    return to_update

  @classmethod
  def __get_raw__(cls):
    """
    Gets all package default.json files and project default.json files and merges them all into one dictionary.
    This dictionary is saved to :variable:`cls.raw` which can be access by a setter method.
    """
    cls.out_default: dict = {}
    cls.package_root = Path(__file__).parent

    # Check for venv
    if not cls.__exists__("./venv"):
      console.error(f"No \"Venv\" dir found in root, this is needed to run siblink at all...")
      quit()

    # Set Values
    cls.raw = {}
    cls.venv = Path("./venv")
    cls.root = cls.venv.parent
    cls.python_exe: Path = cls.venv / cls.os_switch / "python.exe"
    cls.pip_exe: Path = cls.venv / cls.os_switch / "pip.exe"

    # Get default.json files from package
    package_defaults: List[str] = glob.glob(f"{cls.package_root / 'defaults'}/*.default.json")
    for package_default in package_defaults:
      merge = cls.__get_dict__(package_default, "package defaults")
      cls.out_default.update(merge)

    # Get default.json files from project
    project_defaults: List[str] = glob.glob(f"{cls.root / 'defaults'}/*.default.json")
    for project_default in project_defaults:
      merge = cls.__get_dict__(project_default, "project defaults")
      cls.out_default.update(merge)

    res: Union[dict, None] = {}

    if cls.__exists__("./config.json"):
      res = cls.__get_dict__(cls.root / "config.json", "config getter", none_on_fail=True)
      if res is None:
        console.warn(f"Failed to parse {(cls.root / 'config.json').absolute()}... Overwriting")
      res = {}
      Path("./config.json").write_text("{}")
      cls.raw = cls.deep_update(cls.out_default, res)

    Path(cls.root / "config.json").write_text(json.dumps(cls.raw, indent=2))

  @classmethod
  def __exists__(cls, path: str) -> bool:
    """
    Inherited method from pathlib.Path(path).exists()
    :arg path: str: String representation of a path
    """
    return Path(path).exists()

  @classmethod
  def __get_dict__(cls, path: Union[Path, str], caller: str = "", raise_on_fail: bool = False, none_on_fail: bool = False) -> dict:
    """
    Attempts to decode a json file, returns Nothing on fail if :arg:`none_on_fail` is True, raises an error on fail if :arg:`raise_on_fail` is True.
    :arg path: Union[Path, str]: Path object of json file
    :arg caller: str = "": Identifier used in debugging and error handling
    :arg raise_on_fail: bool = False: Determines whether this method raises an error if the json decoding fails
    :arg none_on_fail: bool = False: Determines whether this method returns a NoneType object if the json decoding fails
    """
    try:
      return json.loads(Path(path).read_text())
    except json.JSONDecodeError as json_error:
      console.error(f"Failed to parse json in {Path(path).name} of {caller}")
      if raise_on_fail:
        raise json_error
      if none_on_fail:
        return None
      return {}


Config()
