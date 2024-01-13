import click
from siblink.commands.init import init
from siblink.commands.install import install
from siblink.commands.run import run


@click.group()
def cli():
  """Cli Entry"""
  pass


# Add Commands
cli.add_command(init)
cli.add_command(install)
cli.add_command(run)


def main():
  """Setup.py Entry"""
  cli()


# Run Entry
if __name__ == "__main__":
  main()
