import click
from pyucc import console


@click.command()
def init():
  """
  [init] Testing Documentation
  """
  console.info("[init]")
