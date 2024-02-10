import click
from pyucc import console
from siblink import Config


@click.command()
@click.argument("script_name")
@Config.load_predetermined
def script():
  """
  [script]
  """

  return
