from pathlib import Path
from typing import Optional, Any
import os
import json
from pyucc import colors, console


config_template = {
    "siblink": {
        "venv": "./venv",
        "scripts": {
            "$parent": "./scripts",
            "initial": "$/initial.py",
            "start": "$/start.py",
            "install": "$/install_script.py",
            "clean": "$/clean.py",
            "test": "$/test.py"
        }
    },
    "trelbot": {
        "token": "$yourtokenhere"
    },
    "backend": {
        "port": 2817,
        "ssl": "./ssl",
        "blueprints": {
            "$parent": "./backend/api",
            "@me": {
                "location": "$/@me"
            },
            "@others": {
                "location": "$/@others"
            }
        }
    }
}


class HasRequiredValues:

  def __init__(self, populate: dict, RequiredKeys: dict[str, Any]) -> None:
    """
    Object which contains two variables to check and look over inputted dictionary information.
    Checks if values exists within the supplied dictionary and also checks the values type.
    If one or more values are missing then a `NotImplementedError` will be raised, otherwise, all good!

    :arg populate: dict: The dictionary which will be checked for values
    :arg RequiredKeys: dict[str, any]: A dictionary or object containing string key value pairs. The values must be able to be used in isinstance
    """

    for k, v in populate.items():
      if k in RequiredKeys:
        key_type = RequiredKeys.pop(k)
        if not isinstance(v, key_type):
          raise TypeError(f"\"{k}\" in RequiredKeys is not of type {key_type} instead its {v}")
        setattr(self, k, v)

    for missed_child in RequiredKeys.keys():
      print(f"Missing the required value {missed_child}")

    if RequiredKeys:
      raise NotImplementedError("Missing one or more required values.")


class ScriptHandler:

  @classmethod
  def get(cls, script_name: str):
    """
    Method is used to get the path of a inputted script variable, this script variable could be a name or a direct or relative path
    to a script. Local scripts or script names should be saved in config.json within siblink and scripts.
    :arg script_name: str: The script to be converted
    """

    parent = Config.siblink.scripts.get("$parent", None)

    if not script_name in Config.siblink.scripts:
      path: Path = Path(script_name)

      if not path.exists():
        console.error(f"\"{script_name}\" is not found within {colors.vibrant_violet}siblink.conf{colors.vibrant_red} under a script header nor is it a file...")
        quit()

      return path

    script_path_in_config: str = Config.siblink.scripts.get(script_name)
    if parent is not None:
      script_path_in_config = script_path_in_config.replace("$", parent, 1)

    script_path: Path = Path(script_path_in_config)

    if not script_path.exists():
      console.error(f"\"{script_name}\" contains invalid or not found {colors.vibrant_violet}path{colors.vibrant_yellow} {script_path.absolute()}")
      quit()

    return script_path


class BlueprintHandler:

  @classmethod
  def get_all(cls) -> list[Path]:
    """
    Finds all blueprints mentioned or referenced within `config.json`, these blueprints are then parsed and added
    to a list which this method will return.
    """
    blueprints = dict(Config.backend.blueprints)
    parent = blueprints.pop("$parent", None)
    buff: list[str] = []

    for blueprint_data in blueprints.values():
      location = blueprint_data.get("location")

      if parent:
        location = location.replace("$", parent, 1)

      if not location.endswith(".py"):
        location += ".py"

      location: Path = Path(location)

      if not location.exists():
        console.error(f"Location {location.absolute()} does not exist.")
        return

      buff.append(location)

    return buff


class Config:

  os_switch: str = 'Scripts' if os.name == 'nt' else 'bin'

  def __init__(self) -> None:
    if not hasattr(Config, "loaded"):
      Config.__load__()

  @classmethod
  def __generate__(cls) -> None:
    """
    Generate a :file:`./config.json` file which takes from :file:`./config.default` if it exists, else `{}`. As of right now, :file:`./config.default` is of the json format, but im thinking
    of changing it into another file format such as yaml... Its redundant but maybe it holds water.
    """
    json_out: Optional[dict] = {}
    config_default_path: Path = Path("./config.default")
    config_json_path: Path = Path("./config.json")

    if cls.__exists__("./config.default"):
      try:
        json_out = json.loads(config_default_path.read_text())
      except json.JSONDecodeError:
        pass

    if not cls.__exists__("./config.json"):
      config_json_path.write_text(json.dumps(json_out, indent=4))

    return json_out

  @classmethod
  def __exists__(cls, path: str) -> bool:
    """
    Inherited method from pathlib.Path(path).exists()
    :arg path: str: String representation of a path
    """
    return Path(path).exists()

  @classmethod
  def __values__(cls) -> any:
    """
    Supposed to simulate cls.__dict__ but without all the other methods, used to represent its core values.
    """
    keys = ["siblink", "trelbot", "backend"]
    buff: dict = {}
    for key in keys:
      if key in cls.__dict__:
        buff.__setitem__(key, cls.__dict__.get(key).__dict__)
    return buff

  @classmethod
  def __settle__(cls) -> None:
    """
    Caches important paths into this object, these paths include `root`, `siblink_venv`, `python_exe`, and `pip_exe`
    """

    siblink_venv: Path = Path(cls.siblink.venv)

    if not siblink_venv.exists():
      console.error(f"{colors.vibrant_violet}venv/{colors.vibrant_red} value specified doesn't exist... {colors.vibrant_yellow}{siblink_venv.absolute()}{colors.vibrant_red}")
      quit()

    python_exe: Path = siblink_venv / cls.os_switch / "python.exe"
    pip_exe: Path = siblink_venv / cls.os_switch / "pip.exe"

    if not python_exe.exists():
      console.error(f"{colors.vibrant_violet}venv/python.exe{colors.vibrant_red} is not discoverable with current {colors.vibrant_yellow}configuration{colors.vibrant_red}")
      quit()

    if not pip_exe.exists():
      console.error(f"{colors.vibrant_violet}venv/pip.exe{colors.vibrant_red} is not discoverable with current {colors.vibrant_yellow}configuration{colors.vibrant_red}")
      quit()

    cls.root = siblink_venv.parent
    cls.siblink_venv = siblink_venv
    cls.python_exe = python_exe
    cls.pip_exe = pip_exe

  @classmethod
  def __load__(cls, path: Optional[str] = None) -> dict:
    """
    Loads the config.json file if it exists, if not it will create it. The data from
    the config.json file will be saved in memory and converted into an object which can be used anywhere
    :arg path: Optional[str] = None: Path of the `config.json` file, defaults to none. If no path is specified, will use "./config.json" as path.
    """
    cls.BlueprintHandler = BlueprintHandler
    cls.ScriptHandler = ScriptHandler
    cls.loaded: bool = True

    cls.__generate__()
    path: Path = Path("./config.json")

    ConfigAsDict: dict = json.loads(path.read_text(encoding="UTF-8"))

    cls.siblink = HasRequiredValues(ConfigAsDict.get("siblink"), {
        "venv": str,
        "scripts": dict
    })

    cls.trelbot = HasRequiredValues(ConfigAsDict.get("trelbot"), {
        "token": str
    })

    cls.backend = HasRequiredValues(ConfigAsDict.get("backend"), {
        "port": int,
        "ssl": str,
        "blueprints": dict
    })

    cls.__settle__()


Config()
