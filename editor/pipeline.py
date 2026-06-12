import json
from editor.result import OperationResult, PipelineResult
from editor.resize import process_resize
from editor.enhance import process_enhance
from editor.optimize import process_optimize, persist


def run_pipeline(
    img,
    input_path: str,
    output_path: str,
    steps_json: str,
) -> PipelineResult:
    steps = json.loads(steps_json)
    diffs: list[OperationResult] = []
    save_kwargs = {}

    for step in steps:
        op = step.get("op")
        if op == "resize":
            img, result = process_resize(
                img,
                width=step.get("width"),
                height=step.get("height"),
                scale=step.get("scale"),
                keep_ratio=step.get("keep_ratio", True),
                resample=step.get("resample", "LANCZOS"),
            )
            diffs.append(OperationResult(
                output_path=output_path,
                input_path=input_path,
                changes=result,
            ))
        elif op == "optimize":
            img, result = process_optimize(
                img,
                input_path,
                quality=step.get("quality", 80),
                target_format=step.get("target_format"),
                strip_metadata=step.get("strip_metadata", False),
                progressive=step.get("progressive", False),
            )
            save_kwargs["format"] = result["format"]["new"]
            save_kwargs["quality"] = step.get("quality", 80)
            save_kwargs["progressive"] = step.get("progressive", False)
            diffs.append(OperationResult(
                output_path=output_path,
                input_path=input_path,
                changes=result,
            ))
        elif op == "enhance":
            img, result = process_enhance(
                img,
                brightness=step.get("brightness", 1.0),
                contrast=step.get("contrast", 1.0),
                sharpness=step.get("sharpness", 1.0),
                saturation=step.get("saturation", 1.0),
                auto_enhance=step.get("auto_enhance", False),
                denoise=step.get("denoise", False),
                grayscale=step.get("grayscale", False),
            )
            diffs.append(OperationResult(
                output_path=output_path,
                input_path=input_path,
                changes=result,
            ))
        else:
            raise ValueError(f"Unknown Operation: {op}")

    save_result = persist(
        img,
        output_path,
        output_format=save_kwargs.get("format"),
        quality=save_kwargs.get("quality", 80),
        progressive=save_kwargs.get("progressive", False),
    )

    if diffs and "format" in diffs[-1].changes:
        diffs[-1].changes["size"] = save_result.changes["size"]

    return PipelineResult(output_path=output_path, steps=diffs)
