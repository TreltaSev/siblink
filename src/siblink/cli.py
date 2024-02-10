import click
from siblink.commands.init import init
from siblink.commands.run import run
from siblink.commands.script import script


@click.group()
def cli():
  """Cli Entry"""
  pass


# Add Commands
cli.add_command(init)
cli.add_command(run)
cli.add_command(script)


def main():
  """Setup.py Entry"""
  cli()


# Run Entry
if __name__ == "__main__":
  main()
