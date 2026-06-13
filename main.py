import click
from editor._defaults import QUALITY, RESAMPLE, KEEP_RATIO, PROGRESSIVE, STRIP_METADATA, SUFFIXES
from editor.pipeline import run_pipeline, run_single_op
from editor.tui import run_interactive_tui, run_tui_resize
from utils.display import print_banner, print_success, print_error, print_diff
from utils.runner import run_operation


@click.group(invoke_without_command=True, no_args_is_help=False)
@click.pass_context
def cli(ctx):
    print_banner("1.0.1")
    if ctx.invoked_subcommand is None:
        result = run_interactive_tui()
        if result is not None:
            print_diff(result)


@cli.command(name="resize")
@click.argument("input_path")
@click.option("--width", "-W", default=None, type=int)
@click.option("--height", "-H", default=None, type=int)
@click.option("--scale", "-s", default=None, type=float)
@click.option("--keep-ratio", is_flag=True, default=KEEP_RATIO)
@click.option("--resample", default=RESAMPLE)
@click.option("--output", "-o", default=None)
def resize_cmd(input_path, output, width, height, scale, keep_ratio, resample):
    run_operation(
        input_path, output, SUFFIXES["resize"], run_single_op,
        op="resize",
        width=width, height=height, scale=scale,
        keep_ratio=keep_ratio, resample=resample,
    )


@cli.command(name="optimize")
@click.argument("input_path")
@click.option("--quality", "-q", default=QUALITY, type=int)
@click.option("--target-format", "-t", default=None)
@click.option("--strip-metadata", "-s", is_flag=True, default=STRIP_METADATA)
@click.option("--progressive", "-p", is_flag=True, default=PROGRESSIVE)
@click.option("--output", "-o", default=None)
def optimize_cmd(input_path, output, quality, target_format, strip_metadata, progressive):
    run_operation(
        input_path, output, SUFFIXES["optimize"], run_single_op,
        op="optimize",
        quality=quality, target_format=target_format,
        strip_metadata=strip_metadata, progressive=progressive,
    )


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
def enhance_cmd(input_path, output, brightness, contrast, sharpness, saturation, auto, denoise, grayscale):
    run_operation(
        input_path, output, SUFFIXES["enhance"], run_single_op,
        op="enhance",
        brightness=brightness, contrast=contrast,
        sharpness=sharpness, saturation=saturation,
        auto_enhance=auto, denoise=denoise, grayscale=grayscale,
    )


@cli.command(name="pipeline")
@click.argument("input_path")
@click.option("--steps", "-s", default=None)
@click.option("--output", "-o", default=None)
def pipeline_cmd(input_path, output, steps):
    run_operation(
        input_path, output, SUFFIXES["pipeline"], run_pipeline,
        steps_json=steps,
        handle_result=lambda r: [print_diff(s) for s in r.steps],
    )


@cli.command(name="tui")
@click.argument("input_path")
@click.option("--operation", default="resize", type=click.Choice(["resize"]))
@click.option("--width", "-W", default=None, type=int)
@click.option("--height", "-H", default=None, type=int)
@click.option("--scale", "-s", default=None, type=float)
@click.option("--keep-ratio", is_flag=True, default=KEEP_RATIO)
@click.option("--resample", default=RESAMPLE)
@click.option("--output", "-o", default=None)
def tui_cmd(input_path, operation, output, width, height, scale, keep_ratio, resample):
    try:
        if operation == "resize":
            result = run_tui_resize(
                input_path,
                output,
                width=width,
                height=height,
                scale=scale,
                keep_ratio=keep_ratio,
                resample=resample,
            )
            print_success("TUI resize complete")
            print_diff(result)
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    cli()
