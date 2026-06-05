from click.testing import CliRunner
from PIL import Image

from main import cli


def create_input_image(path):
    Image.new("RGB", (1200, 800), color=(255, 0, 0)).save(path)


def test_tui_resize_flow_saves_output_and_reports_success(tmp_path):
    input_path = tmp_path / "input.jpg"
    output_path = tmp_path / "output.jpg"
    create_input_image(input_path)

    result = CliRunner().invoke(
        cli,
        [
            "tui",
            str(input_path),
            "--operation",
            "resize",
            "--width",
            "600",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert "TUI resize complete" in result.output
    assert output_path.exists()
    assert Image.open(output_path).size == (600, 400)
