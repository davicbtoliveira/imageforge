from PIL import Image
from editor.result import OperationResult

RESAMPLE_FILTERS = {
    "LANCZOS": Image.Resampling.LANCZOS,
    "BICUBIC": Image.Resampling.BICUBIC,
    "BILINEAR": Image.Resampling.BILINEAR,
    "NEAREST": Image.Resampling.NEAREST,
}


def process_resize(
    img: Image.Image,
    width: int | None,
    height: int | None,
    scale: float | None,
    keep_ratio: bool,
    resample: str,
) -> tuple[Image.Image, dict]:
    original_width, original_height = img.size
    original_ratio = original_width / original_height
    size = (width, height)

    filter_ = RESAMPLE_FILTERS.get(resample, Image.Resampling.LANCZOS)

    if scale is not None:
        new_h = int(original_height * scale)
        new_w = int(original_width * scale)
        img = img.resize((new_w, new_h), filter_)
    elif width is not None and height is not None:
        if keep_ratio:
            img.thumbnail(size, filter_)
        else:
            img = img.resize(size, filter_)
    elif width is not None and height is None:
        new_w = width
        if keep_ratio:
            new_h = int(width / original_ratio)
        else:
            new_h = original_height
        img = img.resize((new_w, new_h), filter_)
    elif height is not None and width is None:
        new_h = height
        if keep_ratio:
            new_w = int(height * original_ratio)
        else:
            new_w = original_width
        img = img.resize((new_w, new_h), filter_)
    else:
        raise ValueError("Must specify width, height, or scale")

    return img, {
        "dimensions": {"original": (original_width, original_height), "new": img.size},
    }


def resize(
    img: Image.Image,
    input_path: str,
    output_path: str,
    width: int | None,
    height: int | None,
    scale: float | None,
    keep_ratio: bool,
    resample: str,
) -> OperationResult:
    img, result = process_resize(img, width, height, scale, keep_ratio, resample)
    img.save(output_path)
    return OperationResult(
        output_path=output_path,
        input_path=input_path,
        changes=result,
    )
