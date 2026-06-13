import os
import json
from PIL import Image
from shared.result import OperationResult, PipelineResult
from editor._defaults import QUALITY, RESAMPLE, KEEP_RATIO, PROGRESSIVE, STRIP_METADATA
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
                keep_ratio=step.get("keep_ratio", KEEP_RATIO),
                resample=step.get("resample", RESAMPLE),
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
                target_format=step.get("target_format"),
                strip_metadata=step.get("strip_metadata", STRIP_METADATA),
            )
            save_kwargs["format"] = result["format"]["new"]
            save_kwargs["quality"] = step.get("quality", QUALITY)
            save_kwargs["progressive"] = step.get("progressive", PROGRESSIVE)
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
        quality=save_kwargs.get("quality", QUALITY),
        progressive=save_kwargs.get("progressive", PROGRESSIVE),
    )

    if diffs and "format" in diffs[-1].changes:
        diffs[-1].changes["size"] = save_result.changes["size"]

    return PipelineResult(output_path=output_path, steps=diffs)


def run_single_op(
    img: Image.Image,
    input_path: str,
    output_path: str,
    op: str,
    **kwargs,
) -> OperationResult:
    if op == "resize":
        img, changes = process_resize(
            img,
            width=kwargs.get("width"),
            height=kwargs.get("height"),
            scale=kwargs.get("scale"),
            keep_ratio=kwargs.get("keep_ratio", KEEP_RATIO),
            resample=kwargs.get("resample", RESAMPLE),
        )
        persist(img, output_path, None, QUALITY, PROGRESSIVE)
    elif op == "enhance":
        img, changes = process_enhance(
            img,
            brightness=kwargs.get("brightness", 1.0),
            contrast=kwargs.get("contrast", 1.0),
            sharpness=kwargs.get("sharpness", 1.0),
            saturation=kwargs.get("saturation", 1.0),
            auto_enhance=kwargs.get("auto_enhance", False),
            denoise=kwargs.get("denoise", False),
            grayscale=kwargs.get("grayscale", False),
        )
        persist(img, output_path, None, QUALITY, PROGRESSIVE)
    elif op == "optimize":
        original_size = os.path.getsize(input_path)
        img, changes = process_optimize(
            img,
            input_path,
            target_format=kwargs.get("target_format"),
            strip_metadata=kwargs.get("strip_metadata", STRIP_METADATA),
        )
        output_format = changes["format"]["new"]
        quality = kwargs.get("quality", QUALITY)
        progressive = kwargs.get("progressive", PROGRESSIVE)
        save_result = persist(img, output_path, output_format, quality, progressive)
        changes["size"] = {
            "original": original_size,
            "new": save_result.changes["size"]["new"],
        }
    else:
        raise ValueError(f"Unknown operation: {op}")

    return OperationResult(output_path=output_path, input_path=input_path, changes=changes)
