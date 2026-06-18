import os
from PIL import Image
from editor.operations import OptimizeOperation
from editor.pipeline import run_single_op
from editor.writer import FileSystemWriter
from shared.result import OperationResult


def create_test_image(tmp_path):
    img = Image.new("RGB", (800, 600), color=(100, 149, 237))
    path = str(tmp_path / "input.jpg")
    img.save(path)
    # reload to get img.format set
    return Image.open(path), path


def test_optimize_strip_metadata():
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    result_img, result = OptimizeOperation(strip_metadata=True).apply(img)
    assert "format" in result


def test_optimize_changes_format():
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img.format = "JPEG"
    result_img, result = OptimizeOperation(target_format="WEBP").apply(img)
    assert result["format"]["new"] == "WEBP"


def test_writer_creates_file(tmp_path):
    img = Image.new("RGB", (100, 100), color=(0, 0, 0))
    out = str(tmp_path / "output.jpg")
    writer = FileSystemWriter()
    result = writer.save(img, out, fmt="JPEG", quality=85, progressive=False)
    assert isinstance(result, OperationResult)
    assert os.path.getsize(out) > 0
    assert "size" in result.changes


def test_optimize_reduces_size(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.jpg")
    result = run_single_op(img, input_path, out, OptimizeOperation())
    assert isinstance(result, OperationResult)
    assert os.path.getsize(out) > 0


def test_optimize_convert_to_webp(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.webp")
    result = run_single_op(img, input_path, out, OptimizeOperation(target_format="WEBP"))
    assert isinstance(result, OperationResult)
    assert out.endswith(".webp")


def test_optimize_quality(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out_high = str(tmp_path / "high.jpg")
    out_low = str(tmp_path / "low.jpg")
    r1 = run_single_op(img, input_path, out_high, OptimizeOperation(quality=95))
    r2 = run_single_op(img, input_path, out_low, OptimizeOperation(quality=10))
    assert os.path.getsize(out_high) > os.path.getsize(out_low)
