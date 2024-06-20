import click
from pyucc import console
from siblink.commands import CustomCli


@click.command(cls=CustomCli, name="install")
def cli():
  """
  [install] Testing Documentation
  """
  console.info("[install]")
  return
