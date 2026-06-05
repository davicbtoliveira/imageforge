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


def test_no_args_opens_interactive_resize_workflow(tmp_path):
    input_path = tmp_path / "input.jpg"
    output_path = tmp_path / "output.jpg"
    create_input_image(input_path)

    result = CliRunner().invoke(
        cli,
        [],
        input=(
            "resize\n"
            f"{input_path}\n"
            f"{output_path}\n"
            "width\n"
            "600\n"
            "y\n"
            "LANCZOS\n"
        ),
    )

    assert result.exit_code == 0
    assert "Select operation" in result.output
    assert "TUI resize complete" in result.output
    assert output_path.exists()
    assert Image.open(output_path).size == (600, 400)


def test_no_args_can_select_interactive_enhance_workflow(tmp_path):
    input_path = tmp_path / "input.jpg"
    output_path = tmp_path / "output.jpg"
    create_input_image(input_path)

    result = CliRunner().invoke(
        cli,
        [],
        input=(
            "enhance\n"
            f"{input_path}\n"
            f"{output_path}\n"
            "y\n"
            "n\n"
            "y\n"
        ),
    )

    assert result.exit_code == 0
    assert "Select operation" in result.output
    assert "TUI enhance complete" in result.output
    assert output_path.exists()
    assert Image.open(output_path).mode == "L"
