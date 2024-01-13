import os
import json
import glob
import collections
from pathlib import Path
from pyucc import console, colors
from typing import Any, List, Union
from _collections_abc import dict_items
from typing import Any, Optional, Union


class Recursed(dict):

  def __init__(self, data: Optional[Union[dict, Any]] = {}):
    self._raw_ = data

  def recourse(func):
    def wrap(self, *args):
      _raw_: dict = object.__getattribute__(self, "_raw_")
      if args[0] in _raw_:
        _val_: Any = _raw_[args[0]]
        if isinstance(_val_, dict):
          return Recursed(_val_)
        return _val_
      return func(self, *args)
    return wrap

  @recourse
  def __getattribute__(self, *args) -> Any:
    """
    Override `__getitem__` method to point towards `self._raw_` while also turning any dictionary
    values into another :class:`Recursed` Object
    """
    return super().__getattribute__(args[0])

  @recourse
  def __getitem__(self, *args) -> Any:
    """
    Override `__getitem__` method to point towards `self._raw_`
    """
    return super().__getitem__(args[0])

  def __iter__(self):
    """
    Override `__iter__` method to point towards `self._raw_`
    """
    return iter(self._raw_.items())

  def __repr__(self) -> str:
    """
    Override `__repr__` method to point towards `self._raw_`
    """
    return self._raw_.__repr__()

  def items(self) -> dict_items:
    """
    Overrides the `items()` method, converts any dictionary objects within
    `self._raw_` into a :class:`Recursed` Object.
    """
    copied: dict = dict(self._raw_)
    for k, v in copied.items():
      if isinstance(v, dict):
        copied[k] = Recursed(v)
    return copied.items()

  def __contains__(self, __key: object) -> bool:
    """
    Override `__contains__` method to point towards `self._raw_`
    """
    return dict(self._raw_).__contains__(__key)


class ConfigMeta(type):
  """
  WARNING: This should be updated to a class decorator instead

  This class is meant to be used as a :metaclass:, it makes the cls.raw variable
  accessible from cls. its a simple change but this can be hard to debug and really annoying to realize.
  Use at own risk me :)
  """

  def __getattribute__(self, __name: str) -> Any:
    raw: Recursed = object.__getattribute__(self, "raw")
    if __name in raw:
      return raw.__getattribute__(__name)
    return super().__getattribute__(__name)


class Config(metaclass=ConfigMeta):
  """
  Handle, Create, Read, and Generate Config Files
  used interchangeably between programs.
  """
  raw = {}
  os_switch: str = 'Scripts' if os.name == "nt" else "bin"

  def __init__(self) -> None:
    super().__init__()

  @classmethod
  def load_config(cls, func):
    """
    This decorator when present, checks if the config is loaded,
    if it isn't it proceeds to load siblink.config.json into the `Config` object.
    This is here so that you can run certain parts of any program while importing config without having
    to always load siblink.config.json, some instances where its not present can cause problems
    """
    def wrapper(*args, **kwargs):
      if not hasattr(Config, "loaded"):
        Config.__get_raw__()
      return func(*args, **kwargs)
    return wrapper

  @classmethod
  def deep_update(cls, default: Union[dict, collections.abc.Mapping], inp: Union[dict, collections.abc.Mapping]) -> dict:
    """
    Recursive updating of dictionaries, used in the :method:`__get_raw__()` method.
    :arg to_update: Union[dict, collections.abc.Mapping]: The dictionary that will be updated
    :arg data: Union[dict, collections.abc.Mapping]: The dictionary that contains the data that will be implanted into :variable:`to_update`
    """

    for k, v in inp.items():
      if isinstance(v, collections.abc.Mapping):
        default[k] = cls.deep_update(default.get(k, {}), v)
      else:
        default[k] = v
    return default

  @classmethod
  def gather_predetermined(cls, venv_path: str = "./venv"):
    """
    Gets predetermined values outside of siblink.config.json, including venv, root, python_exe and pip_exe,

    Returns 0 if venv is not present, returns 1 if all ok.
    """
    cls.venv = Path(venv_path)

    if not cls.venv.exists():
      return 0

    cls.root = cls.venv.parent
    cls.python_exe: Path = cls.venv / cls.os_switch / "python.exe"
    cls.pip_exe: Path = cls.venv / cls.os_switch / "pip.exe"
    cls.package_root = Path(__file__).parent

    return 1

  @classmethod
  def __get_raw__(cls):
    """
    Gets all package default.json files and project default.json files and merges them all into one dictionary.
    This dictionary is saved to :variable:`cls.raw` which can be access by a setter method.
    """
    console.info("__get_raw__")
    cls.out_default: dict = {}

    # Check for venv
    if not cls.__exists__("./venv"):
      console.error(f"No \"Venv\" dir found in root, this is needed to run siblink at all...")
      quit()

    # Set Values
    cls.gather_predetermined()

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

    # Updating the "default" dict with the current dict
    res: Union[dict, None] = {}
    res = cls.__get_dict__(cls.root / "siblink.config.json", "config getter", none_on_fail=True) or {}
    cls.raw = cls.deep_update(cls.out_default, res)

    # Check if writing is actually needed to minimize the write operations
    if not cls.raw == res:
      Path(cls.root / "siblink.config.json").write_text(json.dumps(cls.raw, indent=2))

    cls.raw = Recursed(cls.raw)
    setattr(Config, "loaded", True)

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
    except Exception as error:
      console.error(f"Failed to parse json in {Path(path).name} of {caller}")
      if raise_on_fail:
        raise error
      if none_on_fail:
        return None
      return {}

  def __getattribute__(self, __name: str) -> Any:
    raw = getattr(Config, "raw")
    if __name in raw:
      return
