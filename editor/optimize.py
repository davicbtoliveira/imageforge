import os
from PIL import Image
from pathlib import Path


def optimize(
    img: Image.Image,
    input_path: str,
    output_path: str,
    quality: int,
    target_format: str | None,
    strip_metadata: bool,
    progressive: bool,
) -> dict:
    original_size = os.path.getsize(input_path)

    ext = Path(input_path).suffix.lstrip(".").upper()
    orig_format = "JPEG" if ext == "JPG" else ext
    output_format = target_format if target_format is not None else orig_format
    try:
        if output_format == "JPEG" and img.mode == "RGBA":
            img = img.convert("RGB")
        if strip_metadata is True:
            clean = Image.new(img.mode, img.size)
            clean.putdata(list(img.getdata()))
            img = clean
        img.save(
            output_path, format=output_format, quality=quality, progressive=progressive
        )
    except Exception as e:
        raise RuntimeError(f"Failed to save image {e}")

    final_size = os.path.getsize(output_path)
    return {
        "output_path": output_path,
        "size": {"original": original_size, "new": final_size},
        "format": {"original": orig_format, "new": output_format},
    }
