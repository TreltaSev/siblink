import click
from pyucc import console
from siblink.commands import CustomCli


@click.group(name="init", cls=CustomCli)
def cli():
  """
  [init] Testing Documentation
  """
  console.info("[init]")


@cli.command(name="test")
def test():
  console.info("[init][test]")
