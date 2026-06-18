from collections.abc import Callable

from collections.abc import Callable

from editor.operations import Operation
from editor.pipeline import run_pipeline, run_single_op
from editor.writer import ImageWriter
from shared.result import OperationResult, PipelineResult
from utils.display import print_error, print_success, print_diff
from utils.file_handler import get_output_path, validate_image


def run_operation(
    input_path: str,
    output: str | None,
    suffix: str,
    operation: Operation,
    *,
    handle_result: Callable[[OperationResult], None] | None = None,
    writer: ImageWriter | None = None,
) -> None:
    try:
        img = validate_image(input_path)
        out = get_output_path(input_path, output, suffix)
        result = run_single_op(img, input_path, out, operation, writer=writer)
        print_success(f"Saved to {out}")
        if handle_result:
            handle_result(result)
        else:
            print_diff(result)
    except Exception as e:
        print_error(str(e))


def run_pipeline_operation(
    input_path: str,
    output: str | None,
    suffix: str,
    steps_json: str,
    writer: ImageWriter | None = None,
) -> None:
    try:
        img = validate_image(input_path)
        out = get_output_path(input_path, output, suffix)
        result = run_pipeline(img, input_path, out, steps_json, writer=writer)
        print_success(f"Saved to {out}")
        for s in result.steps:
            print_diff(s)
    except Exception as e:
        print_error(str(e))
