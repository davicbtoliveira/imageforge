import click
from editor.result import OperationResult


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
    click.echo(click.style(f"  ✔ Success: {message}", fg="green"))


def print_info(message: str) -> None:
    click.echo(click.style(f"  ℹ Info: ${message}", fg="yellow"))


def print_diff(data: OperationResult) -> None:
    ch = data.changes
    if not ch:
        return

    if "dimensions" in ch:
        orig = ch["dimensions"]["original"]
        new = ch["dimensions"]["new"]
        click.echo(
            click.style(
                f"     • Dimensions: {orig[0]}x{orig[1]} → {new[0]}x{new[1]}", fg="cyan"
            )
        )

    if "size" in ch:
        orig = ch["size"]["original"]
        new = ch["size"]["new"]
        if new < orig:
            pct = int((1 - new / orig) * 100)
            click.echo(
                click.style(
                    f"     • Size: {format_bytes(orig)} → {format_bytes(new)} ({pct}% saved)",
                    fg="cyan",
                )
            )
        else:
            click.echo(
                click.style(
                    f"     • Size: {format_bytes(orig)} → {format_bytes(new)}",
                    fg="cyan",
                )
            )

    if "format" in ch:
        orig_fmt = ch["format"]["original"]
        new_fmt = ch["format"]["new"]
        if orig_fmt != new_fmt:
            click.echo(click.style(f"     • Format: {orig_fmt} → {new_fmt}", fg="cyan"))

    if "enhanced" in ch:
        mode = ch["enhanced"]["mode"]
        applied = ch["enhanced"]["applied"]
        if mode == "auto":
            click.echo(
                click.style(f"     • Enhanced: {', '.join(applied)} (auto)", fg="cyan")
            )
        else:
            changes = []
            for key, vals in ch["enhanced"]["changes"].items():
                changes.append(f"{key}: {vals[0]}→{vals[1]}")
            click.echo(click.style(f"     • {', '.join(changes)}", fg="cyan"))


def format_bytes(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"
