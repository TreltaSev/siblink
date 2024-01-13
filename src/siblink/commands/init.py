import click
from pyucc import console
from siblink import Config


@click.command()
@Config.load_predetermined
def init():
  """
  [init] Testing Documentation
  """
  console.info("[init]")
  console.info(f"{Config.venv.exists()}")
