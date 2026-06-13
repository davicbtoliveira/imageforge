from PIL import Image
import click

from shared.result import OperationResult
from editor._defaults import QUALITY, SUFFIXES
from editor.pipeline import run_single_op
from utils.file_handler import get_output_path, validate_image


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
        img, input_path, out, "resize",
        width=width, height=height, scale=scale,
        keep_ratio=keep_ratio, resample=resample,
    )


def run_interactive_tui() -> dict | None:
    click.echo("Select operation")
    operation = click.prompt(
        "Operation",
        type=click.Choice(["resize", "optimize", "enhance", "exit"], case_sensitive=False),
        default="resize",
    ).lower()

    if operation == "exit":
        click.echo("Bye")
        return None

    input_path = click.prompt("Input image path")
    output_path = _blank_to_none(click.prompt("Output path", default="", show_default=False))

    if operation == "resize":
        result = _interactive_resize(input_path, output_path)
        click.echo("TUI resize complete")
        return result

    if operation == "optimize":
        result = _interactive_optimize(input_path, output_path)
        click.echo("TUI optimize complete")
        return result

    result = _interactive_enhance(input_path, output_path)
    click.echo("TUI enhance complete")
    return result


def _interactive_resize(input_path: str, output_path: str | None) -> dict:
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

    return run_tui_resize(
        input_path,
        output_path,
        width=width,
        height=height,
        scale=scale,
        keep_ratio=keep_ratio,
        resample=resample,
    )


def _interactive_optimize(input_path: str, output_path: str | None) -> dict:
    img = validate_image(input_path)
    out = get_output_path(input_path, output_path, SUFFIXES["tui_optimize"])
    quality = click.prompt("Quality", type=int, default=QUALITY)
    target_format = _blank_to_none(
        click.prompt("Target format", default="", show_default=False)
    )
    if target_format is not None:
        target_format = target_format.upper()
    strip_metadata = click.confirm("Strip metadata", default=False)
    progressive = click.confirm("Progressive", default=False)

    return run_single_op(
        img, input_path, out, "optimize",
        quality=quality, target_format=target_format,
        strip_metadata=strip_metadata, progressive=progressive,
    )


def _interactive_enhance(input_path: str, output_path: str | None) -> dict:
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

    return run_single_op(
        img, input_path, out, "enhance",
        brightness=brightness, contrast=contrast,
        sharpness=sharpness, saturation=saturation,
        auto_enhance=auto_enhance, denoise=denoise, grayscale=grayscale,
    )


def _blank_to_none(value: str) -> str | None:
    value = value.strip()
    return value if value else None
