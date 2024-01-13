# pyright: reportUndefinedVariable=false
from typer import Option
from typing import Any, Union, Literal
from typing_extensions import Annotated
from . import __git__, Config
import enum
import subprocess


class Templates(str, enum.Enum):
  python = "python"


@app.command()
def init(
    template: Annotated[Templates, Option(help="The type of project, depending on this value a different project will be made.")] = Templates.python
):
  """
  Initializes your siblink project by running through a series of checks.
  """

  if template == "python":

    if Config.gather_predetermined() == 1:
      console.warn("./venv already present, stopping")
      quit()

    subprocess.run(f"python -m venv venv", shell=True)

    Config.gather_predetermined()

    subprocess.run(f"{Config.pip_exe.absolute()} install -r ./requirements.txt; siblink pd", shell=true)

    console.info("Finished")
  return
