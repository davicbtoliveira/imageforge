from pathlib import Path

from PIL import Image, UnidentifiedImageError


def validate_image(path: str) -> Image.Image:
    try:
        im = Image.open(path)
        im.verify()
        return Image.open(path)
    except UnidentifiedImageError:
        raise ValueError(f"Not a valid image file: {path}")
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")


def get_output_path(input_path: str, output: str | None, suffix: str) -> str:
    if output is not None:
        return output

    p = Path(input_path)
    return str(p.parent / (p.stem + suffix + p.suffix))
