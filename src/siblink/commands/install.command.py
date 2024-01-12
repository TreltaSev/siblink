# pyright: reportUndefinedVariable=false
from typer import Option
from typing import Union
from typing_extensions import Annotated
from . import __git__

def siblink_path_callback(siblink_path: Union[str, None]):
  pass

@app.command()
def install(
  source: Annotated[Union[str, None], Option(callback=siblink_path_callback, help="Path used after pip install . . .")] = __git__,             
  reinstall: Annotated[bool, Option(help="deletes siblink from the selected locations and then installs them.")] = True, 
  in_global: Annotated[bool, Option(help="Installs within global path")] = False,
  in_local: Annotated[bool, Option(help="installs within local venv based on --venv")] = False,
  full: Annotated[bool, Option(help="determines if install command also applies to global path python siblink, overrides --in-local and --in-global")] = False,
  venv: Annotated[str, Option(help="Path to local venv that siblink will be installed to")] = "./venv",
  ):
  """
  Installs the latest version of siblink into a discoverable python virtual environment
  """
  console.info("No actual function, Config Needed")
  return
