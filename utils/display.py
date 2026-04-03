import click


def print_error(message: str) -> None:
    click.echo(click.style(f"  ✖ {message}", fg="red"))


def print_banner(version: float) -> None:
    banner = r"""
  .___                             ___________
  |   | _____ _____     ____   ____\_   _____/__________  ____   ____
  |   |/     \\__  \   / ___\_/ __ \|    __)/  _ \_  __ \/ ___\_/ __ \
  |   |  Y Y  \/ __ \_/ /_/  >  ___/|     \(  <_> )  | \/ /_/  >  ___/
  |___|__|_|  (____  /\___  / \___  >___  / \____/|__|  \___  / \___  >
            \/     \//_____/      \/    \/             /_____/      \/
  """
    click.echo(click.style(f"${banner} v.{version}", fg="cyan", bold=True))


def print_success(message: str) -> None:
    click.echo(click.style("  ✔ Success", fg="green"))


def print_info(message: str) -> None:
    click.echo(click.style(f"  ℹ Info: ${message}", fg="yellow"))
