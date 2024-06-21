import click
from siblink.commands.init import init
from siblink.commands.pip import pip
from siblink.commands.run import run


@click.group()
def cli():
  """Cli Entry"""
  pass


# Add Commands
cli.add_command(init)
cli.add_command(pip)
cli.add_command(run)


def main():
  """Setup.py Entry"""
  cli()


# Run Entry
if __name__ == "__main__":
  main()
