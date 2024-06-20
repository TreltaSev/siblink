import click
from pyucc import console


@click.command()
def install():
  """
  [install] Testing Documentation
  """
  console.info("[install]")
  return
