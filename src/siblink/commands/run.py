import click
from pyucc import console


@click.command()
def run():
  """
  [run] Testing Documentation
  """
  console.info("[run]")
  return
