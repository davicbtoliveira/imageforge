from PIL import Image
import click
from rich.console import Console
from rich.panel import Panel

from shared.result import OperationResult
from editor._defaults import SUFFIXES
from editor.operations import EnhanceOperation, OptimizeOperation, ResizeOperation
from editor.pipeline import run_single_op
from utils.file_handler import get_output_path, validate_image

console = Console()


def run_tui_resize(
    input_path: str,
    output_path: str | None,
    width: int | None,
    height: int | None,
    scale: float | None,
    keep_ratio: bool,
    resample: str,
) -> OperationResult:
    img: Image.Image = validate_image(input_path)
    out = get_output_path(input_path, output_path, SUFFIXES["tui_resize"])

    return run_single_op(
        img, input_path, out,
        ResizeOperation(width=width, height=height, scale=scale, keep_ratio=keep_ratio, resample=resample),
    )


def run_interactive_tui() -> OperationResult | None:
    console.print(Panel("[bold]Select operation[/bold]", border_style="cyan"))
    operation = click.prompt(
        "Operation",
        type=click.Choice(["resize", "optimize", "enhance", "exit"], case_sensitive=False),
        default="resize",
    ).lower()

    if operation == "exit":
        console.print("[yellow]Bye![/yellow]")
        return None

    input_path = click.prompt("Input image path")
    output_path = _blank_to_none(click.prompt("Output path", default="", show_default=False))

    if operation == "resize":
        result = _interactive_resize(input_path, output_path)
        console.print("[bold green]TUI resize complete[/bold green]")
        return result

    if operation == "optimize":
        result = _interactive_optimize(input_path, output_path)
        console.print("[bold green]TUI optimize complete[/bold green]")
        return result

    result = _interactive_enhance(input_path, output_path)
    console.print("[bold green]TUI enhance complete[/bold green]")
    return result


def _interactive_resize(input_path: str, output_path: str | None) -> OperationResult:
    mode = click.prompt(
        "Resize by",
        type=click.Choice(["width", "height", "scale", "exact"], case_sensitive=False),
        default="width",
    ).lower()
    width = height = scale = None

    if mode == "width":
        width = click.prompt("Width", type=int)
    elif mode == "height":
        height = click.prompt("Height", type=int)
    elif mode == "scale":
        scale = click.prompt("Scale", type=float)
    else:
        width = click.prompt("Width", type=int)
        height = click.prompt("Height", type=int)

    keep_ratio = click.confirm("Keep aspect ratio", default=True)
    resample = click.prompt(
        "Resample filter",
        type=click.Choice(["LANCZOS", "BICUBIC", "BILINEAR", "NEAREST"], case_sensitive=False),
        default="LANCZOS",
    ).upper()

    with console.status("[bold green]Resizing...[/bold green]"):
        return run_tui_resize(
            input_path,
            output_path,
            width=width,
            height=height,
            scale=scale,
            keep_ratio=keep_ratio,
            resample=resample,
        )


def _interactive_optimize(input_path: str, output_path: str | None) -> OperationResult:
    img = validate_image(input_path)
    out = get_output_path(input_path, output_path, SUFFIXES["tui_optimize"])
    quality = click.prompt("Quality", type=int, default=85)
    target_format = _blank_to_none(
        click.prompt("Target format", default="", show_default=False)
    )
    if target_format is not None:
        target_format = target_format.upper()
    strip_metadata = click.confirm("Strip metadata", default=False)
    progressive = click.confirm("Progressive", default=False)

    with console.status("[bold green]Optimizing...[/bold green]"):
        return run_single_op(
            img, input_path, out,
            OptimizeOperation(quality=quality, target_format=target_format, strip_metadata=strip_metadata, progressive=progressive),
        )


def _interactive_enhance(input_path: str, output_path: str | None) -> OperationResult:
    img = validate_image(input_path)
    out = get_output_path(input_path, output_path, SUFFIXES["tui_enhance"])
    auto_enhance = click.confirm("Auto enhance", default=True)

    brightness = contrast = sharpness = saturation = 1.0
    if not auto_enhance:
        brightness = click.prompt("Brightness", type=float, default=1.0)
        contrast = click.prompt("Contrast", type=float, default=1.0)
        sharpness = click.prompt("Sharpness", type=float, default=1.0)
        saturation = click.prompt("Saturation", type=float, default=1.0)

    denoise = click.confirm("Denoise", default=False)
    grayscale = click.confirm("Grayscale", default=False)

    with console.status("[bold green]Enhancing...[/bold green]"):
        return run_single_op(
            img, input_path, out,
            EnhanceOperation(brightness=brightness, contrast=contrast, sharpness=sharpness, saturation=saturation, auto_enhance=auto_enhance, denoise=denoise, grayscale=grayscale),
        )


def _blank_to_none(value: str) -> str | None:
    value = value.strip()
    return value if value else None
