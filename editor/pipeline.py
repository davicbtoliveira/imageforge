import json
import os
from typing import Any

from PIL import Image

from editor._defaults import KEEP_RATIO, PROGRESSIVE, QUALITY, RESAMPLE, STRIP_METADATA
from editor.operations import (
    EnhanceOperation,
    Operation,
    OptimizeOperation,
    ResizeOperation,
)
from editor.writer import FileSystemWriter, ImageWriter
from shared.result import OperationResult, PipelineResult


def _step_to_operation(step: dict[str, Any]) -> Operation:
    op = step.get("op")
    if op == "resize":
        return ResizeOperation(
            width=step.get("width"),
            height=step.get("height"),
            scale=step.get("scale"),
            keep_ratio=step.get("keep_ratio", KEEP_RATIO),
            resample=step.get("resample", RESAMPLE),
        )
    if op == "optimize":
        return OptimizeOperation(
            quality=step.get("quality", QUALITY),
            target_format=step.get("target_format"),
            strip_metadata=step.get("strip_metadata", STRIP_METADATA),
            progressive=step.get("progressive", PROGRESSIVE),
        )
    if op == "enhance":
        return EnhanceOperation(
            brightness=step.get("brightness", 1.0),
            contrast=step.get("contrast", 1.0),
            sharpness=step.get("sharpness", 1.0),
            saturation=step.get("saturation", 1.0),
            auto_enhance=step.get("auto_enhance", False),
            denoise=step.get("denoise", False),
            grayscale=step.get("grayscale", False),
        )
    raise ValueError(f"Unknown Operation: {op}")


def run_pipeline(
    img: Image.Image,
    input_path: str,
    output_path: str,
    steps_json: str,
    writer: ImageWriter | None = None,
) -> PipelineResult:
    writer = writer or FileSystemWriter()
    steps_data = json.loads(steps_json)
    diffs: list[OperationResult] = []
    operations = [_step_to_operation(s) for s in steps_data]
    accumulated_save_options: dict[str, Any] = {}

    for op in operations:
        img, changes = op.apply(img)
        accumulated_save_options.update(changes.get("save_options", {}))
        diffs.append(OperationResult(
            output_path=output_path,
            input_path=input_path,
            changes=changes,
        ))

    save_result = writer.save(
        img,
        output_path,
        fmt=accumulated_save_options.get("format"),
        quality=accumulated_save_options.get("quality", QUALITY),
        progressive=accumulated_save_options.get("progressive", PROGRESSIVE),
    )

    if diffs and "size" in save_result.changes:
        diffs[-1].changes["size"] = save_result.changes["size"]

    return PipelineResult(output_path=output_path, steps=diffs)


def run_single_op(
    img: Image.Image,
    input_path: str,
    output_path: str,
    operation: Operation,
    writer: ImageWriter | None = None,
) -> OperationResult:
    writer = writer or FileSystemWriter()

    img, changes = operation.apply(img)
    save_options = changes.get("save_options", {})
    save_result = writer.save(
        img,
        output_path,
        fmt=save_options.get("format"),
        quality=save_options.get("quality", QUALITY),
        progressive=save_options.get("progressive", PROGRESSIVE),
    )

    if input_path and os.path.exists(input_path):
        original_size = os.path.getsize(input_path)
        new_size = save_result.changes.get("size", {}).get("new")
        if new_size is not None:
            changes["size"] = {"original": original_size, "new": new_size}

    return OperationResult(output_path=output_path, input_path=input_path, changes=changes)
