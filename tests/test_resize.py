from PIL import Image
from editor.operations import ResizeOperation
from editor.pipeline import run_single_op
from shared.result import OperationResult


def create_test_image():
    return Image.new("RGB", (1200, 800), color=(255, 0, 0))


def test_resize_by_width():
    img, result = ResizeOperation(width=600).apply(create_test_image())
    assert img.size == (600, 400)
    assert result["dimensions"]["original"] == (1200, 800)


def test_resize_by_scale():
    img, result = ResizeOperation(scale=0.5).apply(create_test_image())
    assert img.size == (600, 400)


def test_resize_exact():
    img, result = ResizeOperation(width=640, height=480, keep_ratio=False).apply(create_test_image())
    assert img.size == (640, 480)


def test_resize_thumbnail_fits_box():
    img, result = ResizeOperation(width=600, height=400, keep_ratio=True).apply(create_test_image())
    assert img.size == (600, 400)


def test_resize_by_height():
    img, result = ResizeOperation(height=400).apply(create_test_image())
    assert img.size == (600, 400)


def test_resize_no_params_errors():
    import pytest
    with pytest.raises(ValueError, match="Must specify width, height, or scale"):
        ResizeOperation().apply(create_test_image())


def test_run_single_op_resize(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = run_single_op(create_test_image(), "", out, ResizeOperation(width=600))
    assert isinstance(result, OperationResult)
    assert result.output_path == out
    img = Image.open(result.output_path)
    assert img.size == (600, 400)
