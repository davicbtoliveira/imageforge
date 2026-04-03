import os
from PIL import Image
from editor.enhance import enhance


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


def test_enhance_auto(tmp_path):
    out = str(tmp_path / "output.jpg")
    enhance(create_test_image(), "", out, **
            {**DEFAULT_ENHANCE, "auto_enhance": True})
    assert os.path.exists(out)


def test_enhance_grayscale(tmp_path):
    out = str(tmp_path / "output.jpg")
    enhance(create_test_image(), "", out, **
            {**DEFAULT_ENHANCE, "grayscale": True})
    assert Image.open(out).mode == "L"


def test_enhance_brightness(tmp_path):
    out = str(tmp_path / "output.jpg")
    enhance(create_test_image(), "", out, **
            {**DEFAULT_ENHANCE, "brightness": 1.5})
    os.path.exists(out)
