import json
from PIL import Image
from editor.resize import resize
from editor.enhance import enhance
from editor.optimize import optimize


def run_pipeline(
    img: Image.Image,
    input_path: str,
    output_path: str,
    steps_json: str,
) -> dict:
    steps = json.loads(steps_json)
    diffs = []

    for step in steps:
        op = step.get("op")
        if op == "resize":
            result = resize(
                img,
                input_path,
                output_path,
                width=step.get("width"),
                height=step.get("height"),
                scale=step.get("scale"),
                keep_ratio=step.get("keep_ratio", False),
                resample=step.get("resample", "LANCZOS"),
            )
            diffs.append(result)
            img = Image.open(output_path)
        elif op == "optimize":
            result = optimize(
                img,
                input_path,
                output_path,
                quality=step.get("quality", 80),
                target_format=(step.get("target_format")),
                strip_metadata=step.get("strip_metadata", False),
                progressive=step.get("progressive", False),
            )
            diffs.append(result)
            img = Image.open(output_path)
        elif op == "enhance":
            result = enhance(
                img,
                input_path,
                output_path,
                brightness=step.get("brightness", 1.0),
                contrast=step.get("contrast", 1.0),
                sharpness=step.get("sharpness", 1.0),
                saturation=step.get("saturation", 1.0),
                auto_enhance=step.get("auto_enhance", False),
                denoise=step.get("denoise", False),
                grayscale=step.get("grayscale", False),
            )
            diffs.append(result)
            img = Image.open(output_path)
        else:
            raise ValueError(f"Unknown Operation: {op}")

    return {"output_path": output_path, "steps": diffs}
