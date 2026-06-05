from PIL import Image

from editor.enhance import enhance
from editor.optimize import optimize
from editor.pipeline import run_pipeline
from editor.resize import resize
from utils.file_handler import get_output_path, validate_image


def run_tui_resize(
    input_path: str,
    output_path: str | None,
    width: int | None,
    height: int | None,
    scale: float | None,
    keep_ratio: bool,
    resample: str,
) -> dict:
    img: Image.Image = validate_image(input_path)
    out = get_output_path(input_path, output_path, "_tui_resized")

    return resize(
        img,
        input_path,
        out,
        width=width,
        height=height,
        scale=scale,
        keep_ratio=keep_ratio,
        resample=resample,
    )


def run_tui_enhance(
    input_path: str,
    output_path: str | None,
    brightness: float,
    contrast: float,
    sharpness: float,
    saturation: float,
    auto_enhance: bool,
    denoise: bool,
    grayscale: bool,
) -> dict:
    img: Image.Image = validate_image(input_path)
    out = get_output_path(input_path, output_path, "_tui_enhanced")

    return enhance(
        img,
        input_path,
        out,
        brightness=brightness,
        contrast=contrast,
        sharpness=sharpness,
        saturation=saturation,
        auto_enhance=auto_enhance,
        denoise=denoise,
        grayscale=grayscale,
    )


def run_tui_optimize(
    input_path: str,
    output_path: str | None,
    quality: int,
    target_format: str | None,
    strip_metadata: bool,
    progressive: bool,
) -> dict:
    img: Image.Image = validate_image(input_path)
    out = get_output_path(input_path, output_path, "_tui_optimized")

    return optimize(
        img,
        input_path,
        out,
        quality=quality,
        target_format=target_format,
        strip_metadata=strip_metadata,
        progressive=progressive,
    )


def run_tui_pipeline(
    input_path: str,
    output_path: str | None,
    steps: str,
) -> dict:
    img: Image.Image = validate_image(input_path)
    out = get_output_path(input_path, output_path, "_tui_final")

    return run_pipeline(img, input_path, out, steps)


def render_before_after(input_path: str, result: dict) -> str:
    lines = [
        "Before -> After",
        f"Before: {input_path}",
        f"After: {result['output_path']}",
    ]

    results = result.get("steps", [result])

    for step_result in results:
        lines.extend(_render_result_metadata(step_result))

    return "\n".join(lines)


def _render_result_metadata(result: dict) -> list[str]:
    lines = []
    dimensions = result.get("dimensions")
    if dimensions is not None:
        original = dimensions["original"]
        new = dimensions["new"]
        lines.append(
            f"Dimensions: {original[0]}x{original[1]} -> {new[0]}x{new[1]}"
        )

    size = result.get("size")
    if size is not None:
        lines.append(f"Size: {size['original']} -> {size['new']}")

    format_change = result.get("format")
    if format_change is not None:
        lines.append(f"Format: {format_change['original']} -> {format_change['new']}")

    enhanced = result.get("enhanced")
    if enhanced is not None:
        for name, values in enhanced["changes"].items():
            lines.append(f"{name}: {values[0]} -> {values[1]}")

    return lines
