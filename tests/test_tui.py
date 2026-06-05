from click.testing import CliRunner
from PIL import Image

from main import cli


def create_input_image(path):
    Image.new("RGB", (1200, 800), color=(255, 0, 0)).save(path)


def test_cli_help_lists_tui_entry_point():
    result = CliRunner().invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "tui" in result.output


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


def test_tui_resize_flow_shows_before_after_fallback(tmp_path):
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
    assert "Before -> After" in result.output
    assert f"Before: {input_path}" in result.output
    assert f"After: {output_path}" in result.output
    assert "Dimensions: 1200x800 -> 600x400" in result.output


def test_tui_enhance_flow_saves_output_and_shows_changes(tmp_path):
    input_path = tmp_path / "input.jpg"
    output_path = tmp_path / "output.jpg"
    create_input_image(input_path)

    result = CliRunner().invoke(
        cli,
        [
            "tui",
            str(input_path),
            "--operation",
            "enhance",
            "--brightness",
            "1.5",
            "--contrast",
            "1.2",
            "--grayscale",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert "TUI enhance complete" in result.output
    assert "Before -> After" in result.output
    assert "brightness: 1.0 -> 1.5" in result.output
    assert "contrast: 1.0 -> 1.2" in result.output
    assert "grayscale: False -> True" in result.output
    assert output_path.exists()
    assert Image.open(output_path).mode == "L"


def test_tui_enhance_flow_reports_invalid_image_without_crashing(tmp_path):
    missing_path = tmp_path / "missing.jpg"

    result = CliRunner().invoke(
        cli,
        ["tui", str(missing_path), "--operation", "enhance", "--brightness", "1.5"],
    )

    assert result.exit_code == 0
    assert "File not found" in result.output


def test_tui_optimize_flow_saves_output_and_shows_size_and_format(tmp_path):
    input_path = tmp_path / "input.jpg"
    output_path = tmp_path / "output.webp"
    create_input_image(input_path)

    result = CliRunner().invoke(
        cli,
        [
            "tui",
            str(input_path),
            "--operation",
            "optimize",
            "--quality",
            "80",
            "--target-format",
            "WEBP",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert "TUI optimize complete" in result.output
    assert "Before -> After" in result.output
    assert "Format: JPEG -> WEBP" in result.output
    assert "Size:" in result.output
    assert output_path.exists()


def test_tui_pipeline_flow_saves_output_and_shows_step_metadata(tmp_path):
    input_path = tmp_path / "input.jpg"
    output_path = tmp_path / "output.jpg"
    create_input_image(input_path)

    result = CliRunner().invoke(
        cli,
        [
            "tui",
            str(input_path),
            "--operation",
            "pipeline",
            "--steps",
            '[{"op":"resize","width":600},{"op":"enhance","grayscale":true}]',
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert "TUI pipeline complete" in result.output
    assert "Before -> After" in result.output
    assert "Dimensions: 1200x800 -> 600x800" in result.output
    assert "grayscale: False -> True" in result.output
    assert output_path.exists()
    assert Image.open(output_path).size == (600, 800)
