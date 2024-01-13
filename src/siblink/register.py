import json
from pathlib import Path


class Register:
  """
  class used to register commands into siblink.cli
  """

  commandsConfiguration: dict = json.loads(Path.read_text(Path(__file__).parent / "commands.json"))

  def __init__(self) -> None:
    pass

  d
