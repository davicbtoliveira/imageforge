import click
from editor.resize import resize
from editor.enhance import enhance
from editor.optimize import optimize
from editor.pipeline import run_pipeline
from utils.file_handler import validate_image, get_output_path
from utils.display import print_banner, print_success, print_error, print_diff


@click.group()
def cli():
    print_banner("1.0.0")


@cli.command(name="resize")
@click.argument("input_path")
@click.option("--width", "-W", default=None, type=int)
@click.option("--height", "-H", default=None, type=int)
@click.option("--scale", "-s", default=None, type=float)
@click.option("--keep-ratio", is_flag=True, default=True)
@click.option("--resample", default="LANCZOS")
@click.option("--output", "-o", default=None)
def resize_cmd(input_path, output, width, height, scale, keep_ratio, resample):
    try:
        img = validate_image(input_path)
        out = get_output_path(input_path, output, "_resized")
        result = resize(
            img, input_path, out, width, height, scale, keep_ratio, resample
        )
        print_success(f"Saved to {out}")
        print_diff(result)
    except Exception as e:
        print_error(str(e))


@cli.command(name="optimize")
@click.argument("input_path")
@click.option("--quality", "-q", default=85, type=int)
@click.option("--target-format", "-t", default=None)
@click.option("--strip-metadata", "-s", is_flag=True, default=False)
@click.option("--progressive", "-p", is_flag=True, default=False)
@click.option("--output", "-o", default=None)
def optimize_cmd(
    input_path, output, quality, target_format, strip_metadata, progressive
):
    try:
        img = validate_image(input_path)
        out = get_output_path(input_path, output, "_optimized")
        result = optimize(
            img, input_path, out, quality, target_format, strip_metadata, progressive
        )
        print_success(f"Saved to {out}")
        print_diff(result)
    except Exception as e:
        print_error(str(e))


@cli.command(name="enhance")
@click.argument("input_path")
@click.option("--brightness", "-b", default=1.0, type=float)
@click.option("--contrast", "-c", default=1.0, type=float)
@click.option("--sharpness", "-S", default=1.0, type=float)
@click.option("--saturation", "-s", default=1.0, type=float)
@click.option("--auto", "-a", is_flag=True, default=False)
@click.option("--denoise", "-d", is_flag=True, default=False)
@click.option("--grayscale", "-g", is_flag=True, default=False)
@click.option("--output", "-o", default=None)
def enhance_cmd(
    input_path,
    output,
    brightness,
    contrast,
    sharpness,
    saturation,
    auto,
    denoise,
    grayscale,
):
    try:
        img = validate_image(input_path)
        out = get_output_path(input_path, output, "_enhanced")
        result = enhance(
            img,
            input_path,
            out,
            brightness,
            contrast,
            sharpness,
            saturation,
            auto_enhance=auto,
            denoise=denoise,
            grayscale=grayscale,
        )
        print_success(f"Saved to {out}")
        print_diff(result)
    except Exception as e:
        print_error(str(e))


@cli.command(name="pipeline")
@click.argument("input_path")
@click.option("--steps", "-s", default=None)
@click.option("--output", "-o", default=None)
def pipeline_cmd(input_path, output, steps):
    try:
        img = validate_image(input_path)
        out = get_output_path(input_path, output, "_final")
        result = run_pipeline(img, input_path, out, steps)
        print_success(f"Saved to {out}")
        for step_result in result.get("steps", []):
            print_diff(step_result)
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    cli()
