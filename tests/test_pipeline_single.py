import os
from PIL import Image
from shared.result import OperationResult
from editor.pipeline import run_single_op


def test_run_single_op_resize(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.jpg")
    Image.new("RGB", (1200, 800), color=(255, 0, 0)).save(input_path)
    img = Image.open(input_path)
    result = run_single_op(img, input_path, output_path, "resize", width=600)
    assert isinstance(result, OperationResult)
    assert result.output_path == output_path
    out = Image.open(output_path)
    assert out.size == (600, 400)


def test_run_single_op_enhance(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.jpg")
    Image.new("RGB", (100, 100), color=(100, 149, 237)).save(input_path)
    img = Image.open(input_path)
    result = run_single_op(img, input_path, output_path, "enhance", grayscale=True)
    assert isinstance(result, OperationResult)
    out = Image.open(output_path)
    assert out.mode == "L"


def test_run_single_op_optimize(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.webp")
    Image.new("RGB", (800, 600), color=(100, 149, 237)).save(input_path)
    img = Image.open(input_path)
    original_size = os.path.getsize(input_path)
    result = run_single_op(
        img, input_path, output_path, "optimize",
        target_format="WEBP", quality=50,
    )
    assert isinstance(result, OperationResult)
    assert os.path.getsize(output_path) > 0
    assert "size" in result.changes
    assert result.changes["size"]["original"] == original_size


def test_run_single_op_unknown(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.jpg")
    Image.new("RGB", (100, 100), color=(255, 0, 0)).save(input_path)
    img = Image.open(input_path)
    try:
        run_single_op(img, input_path, output_path, "unknown")
        assert False, "should raise"
    except ValueError as e:
        assert "unknown" in str(e).lower()
