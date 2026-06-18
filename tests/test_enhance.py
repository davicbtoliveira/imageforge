from PIL import Image
from editor.operations import EnhanceOperation
from editor.pipeline import run_single_op
from shared.result import OperationResult


def create_test_image():
    return Image.new("RGB", (800, 600), color=(100, 149, 237))


def test_grayscale():
    img, result = EnhanceOperation(grayscale=True).apply(create_test_image())
    assert img.mode == "L"
    assert result["enhanced"]["mode"] == "manual"
    assert "grayscale" in result["enhanced"]["applied"]


def test_auto_enhance():
    img, result = EnhanceOperation(auto_enhance=True).apply(create_test_image())
    assert result["enhanced"]["mode"] == "auto"
    assert result["enhanced"]["applied"] == ["brightness", "contrast", "sharpness", "saturation"]


def test_returns_new_image():
    img = create_test_image()
    result_img, result = EnhanceOperation(brightness=1.5).apply(img)
    assert result_img is not img


def test_enhance_auto_integration(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = run_single_op(create_test_image(), "", out, EnhanceOperation(auto_enhance=True))
    assert isinstance(result, OperationResult)
    assert result.output_path == out


def test_enhance_grayscale_integration(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = run_single_op(create_test_image(), "", out, EnhanceOperation(grayscale=True))
    assert Image.open(out).mode == "L"


def test_enhance_brightness_integration(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = run_single_op(create_test_image(), "", out, EnhanceOperation(brightness=1.5))
    assert isinstance(result, OperationResult)
