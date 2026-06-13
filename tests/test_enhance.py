import os
from PIL import Image
from shared.result import OperationResult
from editor.enhance import process_enhance
from editor.pipeline import run_single_op


def create_test_image():
    return Image.new("RGB", (800, 600), color=(100, 149, 237))


DEFAULT_ENHANCE = dict(
    brightness=1.0,
    contrast=1.0,
    sharpness=1.0,
    saturation=1.0,
    auto_enhance=False,
    denoise=False,
    grayscale=False
)


def test_process_enhance_grayscale():
    img = create_test_image()
    result_img, result = process_enhance(img, 1.0, 1.0, 1.0, 1.0, False, False, True)
    assert result_img.mode == "L"
    assert result["enhanced"]["mode"] == "manual"
    assert "grayscale" in result["enhanced"]["applied"]


def test_process_enhance_auto():
    img = create_test_image()
    result_img, result = process_enhance(img, 1.0, 1.0, 1.0, 1.0, True, False, False)
    assert result["enhanced"]["mode"] == "auto"
    assert result["enhanced"]["applied"] == ["brightness", "contrast", "sharpness", "saturation"]


def test_process_enhance_returns_image_in_memory():
    img = create_test_image()
    result_img, result = process_enhance(img, 1.5, 1.0, 1.0, 1.0, False, False, False)
    assert result_img is not img


def test_enhance_auto(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = run_single_op(create_test_image(), "", out, "enhance", **
            {**DEFAULT_ENHANCE, "auto_enhance": True})
    assert isinstance(result, OperationResult)
    assert result.output_path == out
    assert os.path.exists(out)


def test_enhance_grayscale(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = run_single_op(create_test_image(), "", out, "enhance", **
            {**DEFAULT_ENHANCE, "grayscale": True})
    assert isinstance(result, OperationResult)
    assert Image.open(out).mode == "L"


def test_enhance_brightness(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = run_single_op(create_test_image(), "", out, "enhance", **
            {**DEFAULT_ENHANCE, "brightness": 1.5})
    assert isinstance(result, OperationResult)
    assert os.path.exists(out)
