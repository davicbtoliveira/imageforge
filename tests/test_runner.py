import os
from PIL import Image
from shared.result import OperationResult
from utils.runner import run_operation


def test_run_operation_validates_and_runs(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.jpg")
    Image.new("RGB", (100, 100), color=(255, 0, 0)).save(input_path)

    def fake_fn(img, inp, out, **kw):
        img.save(out)
        return OperationResult(output_path=out, input_path=inp)

    run_operation(input_path, output_path, "_resized", fake_fn)
    assert os.path.exists(output_path)
    assert Image.open(output_path).size == (100, 100)
