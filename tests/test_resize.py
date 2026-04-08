from PIL import Image
from editor.resize import resize


def create_test_image():
    img = Image.new("RGB", (1200, 800), color=(255, 0, 0))
    return img


DEFAULT_RESIZE = dict(
    width=None, height=None, scale=None, keep_ratio=True, resample="LANCZOS"
)


def test_resize_by_width(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = resize(create_test_image(), "", out, **{**DEFAULT_RESIZE, "width": 600})
    img = Image.open(result["output_path"])
    assert img.size == (600, 400)


def test_resize_by_scale(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = resize(create_test_image(), "", out, **{**DEFAULT_RESIZE, "scale": 0.5})
    img = Image.open(result["output_path"])
    assert img.size == (600, 400)


def test_resize_exact_dimensions(tmp_path):
    out = str(tmp_path / "output.jpg")
    result = resize(
        create_test_image(),
        "",
        out,
        **{**DEFAULT_RESIZE, "width": 640, "height": 480, "keep_ratio": False},
    )
    img = Image.open(result["output_path"])
    assert img.size == (640, 480)
