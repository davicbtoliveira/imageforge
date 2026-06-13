import os
from PIL import Image
from shared.result import OperationResult
from editor.optimize import process_optimize, persist
from editor.pipeline import run_single_op


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


def test_process_optimize_strip_metadata(tmp_path):
    img, input_path = create_test_image(tmp_path)
    result_img, result = process_optimize(img, input_path, None, True)
    assert "format" in result


def test_process_optimize_changes_format(tmp_path):
    img, input_path = create_test_image(tmp_path)
    result_img, result = process_optimize(img, input_path, "WEBP", False)
    assert result["format"]["new"] == "WEBP"


def test_persist_creates_file(tmp_path):
    img = Image.new("RGB", (100, 100), color=(0, 0, 0))
    out = str(tmp_path / "output.jpg")
    result = persist(img, out, "JPEG", 85, False)
    assert isinstance(result, OperationResult)
    assert os.path.getsize(out) > 0
    assert "size" in result.changes


def test_optimize_reduces_size(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.jpg")
    result = run_single_op(img, input_path, out, "optimize", **DEFAULT_OPTIMIZE)
    assert isinstance(result, OperationResult)
    assert os.path.getsize(out) > 0


def test_optimize_convert_to_webp(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.webp")
    result = run_single_op(img, input_path, out, "optimize", **
             {**DEFAULT_OPTIMIZE, "target_format": "WEBP"})
    assert isinstance(result, OperationResult)
    assert os.path.basename(out).endswith(".webp")


def test_optimize_quality(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out_high = str(tmp_path / "high.jpg")
    out_low = str(tmp_path / "low.jpg")
    r1 = run_single_op(img, input_path, out_high, "optimize", **{**DEFAULT_OPTIMIZE, "quality": 95})
    r2 = run_single_op(img, input_path, out_low,  "optimize", **{**DEFAULT_OPTIMIZE, "quality": 10})
    assert isinstance(r1, OperationResult)
    assert isinstance(r2, OperationResult)
    assert os.path.getsize(out_high) > os.path.getsize(out_low)
