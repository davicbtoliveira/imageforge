from PIL import Image
from editor.result import PipelineResult
from editor.pipeline import run_pipeline


def create_test_image(tmp_path):
    path = str(tmp_path / "input.jpg")
    img = Image.new("RGB", (1200, 800), color=(255, 0, 0))
    img.save(path)
    return img, path


def test_pipeline_resize_only(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.jpg")
    steps = '[{"op":"resize","width":600}]'
    result = run_pipeline(img, input_path, out, steps)
    assert isinstance(result, PipelineResult)
    assert len(result.steps) == 1
    assert Image.open(out).size == (600, 400)


def test_pipeline_resize_enhance(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.jpg")
    steps = (
        '[{"op":"resize","width":600},{"op":"enhance","grayscale":true}]'
    )
    result = run_pipeline(img, input_path, out, steps)
    assert isinstance(result, PipelineResult)
    assert len(result.steps) == 2
    assert Image.open(out).mode == "L"


def test_pipeline_all_three(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.webp")
    steps = (
        '[{"op":"resize","width":600},'
        '{"op":"enhance","brightness":1.2},'
        '{"op":"optimize","quality":80,"target_format":"WEBP"}]'
    )
    result = run_pipeline(img, input_path, out, steps)
    assert isinstance(result, PipelineResult)
    assert len(result.steps) == 3
    out_img = Image.open(out)
    assert out_img.size == (600, 400)
    assert str(out).endswith(".webp")
    assert "size" in result.steps[-1].changes


def test_pipeline_unknown_op(tmp_path):
    img, input_path = create_test_image(tmp_path)
    out = str(tmp_path / "output.jpg")
    steps = '[{"op":"unknown"}]'
    try:
        run_pipeline(img, input_path, out, steps)
        assert False, "should raise"
    except ValueError as e:
        assert "unknown" in str(e).lower()
