from collections.abc import Callable
from typing import Any

from PIL import Image

from shared.result import OperationResult
from utils.display import print_error, print_success, print_diff
from utils.file_handler import get_output_path, validate_image


def run_operation(
    input_path: str,
    output: str | None,
    suffix: str,
    fn: Callable[..., OperationResult],
    *,
    handle_result: Callable[[OperationResult], None] | None = None,
    **fn_kwargs: Any,
) -> None:
    try:
        img = validate_image(input_path)
        out = get_output_path(input_path, output, suffix)
        result = fn(img, input_path, out, **fn_kwargs)
        print_success(f"Saved to {out}")
        if handle_result:
            handle_result(result)
        else:
            print_diff(result)
    except Exception as e:
        print_error(str(e))
