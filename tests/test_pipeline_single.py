import os
from PIL import Image
from editor.operations import EnhanceOperation, OptimizeOperation, ResizeOperation
from editor.pipeline import run_single_op
from shared.result import OperationResult


def test_run_single_op_resize(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.jpg")
    Image.new("RGB", (1200, 800), color=(255, 0, 0)).save(input_path)
    img = Image.open(input_path)
    result = run_single_op(img, input_path, output_path, ResizeOperation(width=600))
    assert isinstance(result, OperationResult)
    assert result.output_path == output_path
    out = Image.open(output_path)
    assert out.size == (600, 400)


def test_run_single_op_enhance(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.jpg")
    Image.new("RGB", (100, 100), color=(100, 149, 237)).save(input_path)
    img = Image.open(input_path)
    result = run_single_op(img, input_path, output_path, EnhanceOperation(grayscale=True))
    assert isinstance(result, OperationResult)
    out = Image.open(output_path)
    assert out.mode == "L"


def test_run_single_op_optimize(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.webp")
    Image.new("RGB", (800, 600), color=(100, 149, 237)).save(input_path)
    img = Image.open(input_path)
    result = run_single_op(img, input_path, output_path, OptimizeOperation(target_format="WEBP", quality=50))
    assert isinstance(result, OperationResult)
    assert os.path.getsize(output_path) > 0
    assert "size" in result.changes
