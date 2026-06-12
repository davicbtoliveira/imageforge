import os
from PIL import Image
from pathlib import Path
from editor.result import OperationResult


def process_optimize(
    img: Image.Image,
    input_path: str,
    quality: int,
    target_format: str | None,
    strip_metadata: bool,
    progressive: bool,
) -> tuple[Image.Image, dict]:
    ext = Path(input_path).suffix.lstrip(".").upper()
    orig_format = "JPEG" if ext == "JPG" else ext
    output_format = target_format if target_format is not None else orig_format

    if output_format == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGB")
    if strip_metadata:
            img = Image.frombytes(img.mode, img.size, img.tobytes())

    return img, {
        "format": {"original": orig_format, "new": output_format},
    }


def persist(
    img: Image.Image,
    output_path: str,
    output_format: str | None,
    quality: int,
    progressive: bool,
) -> OperationResult:
    try:
        img.save(
            output_path,
            format=output_format,
            quality=quality,
            progressive=progressive,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to save image {e}")

    return OperationResult(
        output_path=output_path,
        input_path=output_path,
        changes={"size": {"new": os.path.getsize(output_path)}},
    )


def optimize(
    img: Image.Image,
    input_path: str,
    output_path: str,
    quality: int,
    target_format: str | None,
    strip_metadata: bool,
    progressive: bool,
) -> OperationResult:
    original_size = os.path.getsize(input_path)

    img, result = process_optimize(
        img, input_path, quality, target_format, strip_metadata, progressive
    )

    output_format = result["format"]["new"]
    save_result = persist(img, output_path, output_format, quality, progressive)
    result["size"] = {"original": original_size, "new": save_result.changes["size"]["new"]}
    return OperationResult(
        output_path=output_path,
        input_path=input_path,
        changes=result,
    )
