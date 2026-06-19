from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from shared.result import OperationResult

console = Console()


def print_error(message: str) -> None:
    console.print(f"[red]  ✖ {message}[/red]")


def print_banner(version: float) -> None:
    banner = r"""
  .___                             ___________
  |   | _____ _____     ____   ____\_   _____/__________  ____   ____
  |   |/     \\__  \   / ___\_/ __ \|    __)/  _ \_  __ \/ ___\_/ __ \
  |   |  Y Y  \/ __ \_/ /_/  >  ___/|     \(  <_> )  | \/ /_/  >  ___/
  |___|__|_|  (____  /\___  / \___  >___  / \____/|__|  \___  / \___  >
            \/     \//_____/      \/    \/             /_____/      \/
  """
    content = f"[bold cyan]{banner}[/bold cyan]\n[cyan]v.{version}[/cyan]"
    console.print(Panel(content, border_style="cyan"))


def print_success(message: str) -> None:
    console.print(f"[green]  ✔ Success: {message}[/green]")


def print_info(message: str) -> None:
    console.print(f"[yellow]  ℹ Info: ${message}[/yellow]")


def print_diff(data: OperationResult) -> None:
    ch = data.changes
    if not ch:
        return

    table = Table.grid(padding=(0, 2))
    table.add_column()

    if "dimensions" in ch:
        orig = ch["dimensions"]["original"]
        new = ch["dimensions"]["new"]
        table.add_row(f"Dimensions:  {orig[0]}x{orig[1]}  →  {new[0]}x{new[1]}")

    if "size" in ch:
        orig = ch["size"]["original"]
        new = ch["size"]["new"]
        if new < orig:
            pct = int((1 - new / orig) * 100)
            table.add_row(f"Size:        {format_bytes(orig)}  →  {format_bytes(new)}  ({pct}% saved)")
        else:
            table.add_row(f"Size:        {format_bytes(orig)}  →  {format_bytes(new)}")

    if "format" in ch:
        orig_fmt = ch["format"]["original"]
        new_fmt = ch["format"]["new"]
        if orig_fmt != new_fmt:
            table.add_row(f"Format:      {orig_fmt}  →  {new_fmt}")

    if "enhanced" in ch:
        mode = ch["enhanced"]["mode"]
        applied = ch["enhanced"]["applied"]
        if mode == "auto":
            table.add_row(f"Enhanced:    {', '.join(applied)} (auto)")
        else:
            changes = []
            for key, vals in ch["enhanced"]["changes"].items():
                changes.append(f"{key}: {vals[0]}  →  {vals[1]}")
            table.add_row(" • ".join(changes))

    if table.row_count:
        console.print(Panel(table, title="[bold]Results[/bold]", border_style="cyan"))


def format_bytes(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"
