import click
from pyucc import console
from siblink.commands import CustomCli


@click.command(cls=CustomCli, name="run")
def cli():
  """
  [run] Testing Documentation
  """
  console.info("[run]")
  return
