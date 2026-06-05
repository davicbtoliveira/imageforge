from PIL import Image

from editor.enhance import enhance
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


def render_before_after(input_path: str, result: dict) -> str:
    lines = [
        "Before -> After",
        f"Before: {input_path}",
        f"After: {result['output_path']}",
    ]

    dimensions = result.get("dimensions")
    if dimensions is not None:
        original = dimensions["original"]
        new = dimensions["new"]
        lines.append(
            f"Dimensions: {original[0]}x{original[1]} -> {new[0]}x{new[1]}"
        )

    enhanced = result.get("enhanced")
    if enhanced is not None:
        for name, values in enhanced["changes"].items():
            lines.append(f"{name}: {values[0]} -> {values[1]}")

    return "\n".join(lines)
