# pyright: reportUndefinedVariable=false
from typer import Option, Typer, Context
from typing import Union
from typing_extensions import Annotated


def pd_logic(out: str = "./requirements.txt"):
  console.info("[__pip_dumping__] No Logic")

@app.command()
def pip_dump(
  out: Annotated[str, Option(help="Path to where the the packages will be dumped")] = "./requirements.txt"
  ):
  """
  Dumps all pypi packages into a requirements.txt file, or whatever --out is set to.
  """
  console.info("[pip_dump] No Logic")
  pd_logic(out)
  return

@app.command()
def pd(
  out: Annotated[str, Option(help="Path to where the the packages will be dumped")] = "./requirements.txt"
  ):
  """
  Alias to `siblink pip-dump`
  """
  pd_logic(out)
  return

