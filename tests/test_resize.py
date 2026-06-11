from PIL import Image
from editor.resize import process_resize, resize


def create_test_image():
    img = Image.new("RGB", (1200, 800), color=(255, 0, 0))
    return img


DEFAULT_RESIZE = dict(
    width=None, height=None, scale=None, keep_ratio=True, resample="LANCZOS"
)


def test_process_resize_by_width(tmp_path):
    img, result = process_resize(create_test_image(), 600, None, None, True, "LANCZOS")
    assert img.size == (600, 400)
    assert result["dimensions"]["original"] == (1200, 800)


def test_process_resize_by_scale(tmp_path):
    img, result = process_resize(create_test_image(), None, None, 0.5, True, "LANCZOS")
    assert img.size == (600, 400)


def test_process_resize_exact(tmp_path):
    img, result = process_resize(
        create_test_image(), 640, 480, None, False, "LANCZOS"
    )
    assert img.size == (640, 480)


def test_process_resize_thumbnail_fits_box(tmp_path):
    img, result = process_resize(create_test_image(), 600, 400, None, True, "LANCZOS")
    assert img.size == (600, 400)


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
