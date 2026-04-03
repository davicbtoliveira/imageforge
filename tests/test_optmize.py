import os
from PIL import Image
from editor.optimize import optimize


def create_test_image(tmp_path):
    img = Image.new("RGB", (800, 600), color=(100, 149, 237))
    path = str(tmp_path / "input.jpg")
    img.save(path)
    return img, path


DEFAULT_OPTIMIZE = dict(
    quality=85,
    target_format=None,
    strip_metadata=False,
    progressive=False
)


def test_optimize_reduces_size(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.jpg")
    optimize(img, input_path, out, **DEFAULT_OPTIMIZE)
    assert os.path.getsize(out) > 0


def test_optimize_convert_to_webp(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.webp")
    optimize(img, input_path, out, **
             {**DEFAULT_OPTIMIZE, "target_format": "WEBP"})
    assert os.path.basename(out).endswith(".webp")


def test_optimize_quality(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out_high = str(tmp_path / "high.jpg")
    out_low = str(tmp_path / "low.jpg")
    optimize(img, input_path, out_high, **{**DEFAULT_OPTIMIZE, "quality": 95})
    optimize(img, input_path, out_low,  **{**DEFAULT_OPTIMIZE, "quality": 10})
    assert os.path.getsize(out_high) > os.path.getsize(out_low)
