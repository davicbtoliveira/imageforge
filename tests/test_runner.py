from PIL import Image
from editor.operations import ResizeOperation
from utils.runner import run_operation


def test_run_operation_validates_and_runs(tmp_path):
    input_path = str(tmp_path / "input.jpg")
    output_path = str(tmp_path / "output.jpg")
    Image.new("RGB", (100, 100), color=(255, 0, 0)).save(input_path)

    run_operation(input_path, output_path, "_resized", ResizeOperation(width=50))
    assert Image.open(output_path).size == (50, 50)
