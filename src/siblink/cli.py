from pyucc import console
import click


@click.group
def cli():
  console.info("[cli]")


def main():
  ### Automatic Loading of Commands ###
  # commands_directory = Path(__file__).parent / "commands"
  # commands = [child for child in commands_directory.iterdir() if str(child).endswith(".py")]
  # for command_path in commands:
  #   exec(Path(command_path).read_text())
  cli()


if __name__ == "__main__":
  main()
