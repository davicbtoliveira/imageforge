from PIL import Image, ImageEnhance, ImageFilter


def enhance(
    img: Image.Image,
    input_path: str,
    output_path: str,
    brightness: float,
    contrast: float,
    sharpness: float,
    saturation: float,
    auto_enhance: bool,
    denoise: bool,
    grayscale: bool,
) -> dict:
    defaults = {"brightness": 1.0, "contrast": 1.0, "sharpness": 1.0, "saturation": 1.0}

    if auto_enhance:
        brightness, contrast, sharpness, saturation = 1.2, 1.2, 1.2, 1.2

    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    img = ImageEnhance.Color(img).enhance(saturation)

    applied = []
    changes = {}

    if brightness != 1.0:
        applied.append("brightness")
        changes["brightness"] = (1.0, brightness)
    if contrast != 1.0:
        applied.append("contrast")
        changes["contrast"] = (1.0, contrast)
    if sharpness != 1.0:
        applied.append("sharpness")
        changes["sharpness"] = (1.0, sharpness)
    if saturation != 1.0:
        applied.append("saturation")
        changes["saturation"] = (1.0, saturation)

    if denoise:
        applied.append("denoise")
        changes["denoise"] = (False, True)

    if grayscale:
        applied.append("grayscale")
        changes["grayscale"] = (False, True)

    if auto_enhance:
        applied = ["brightness", "contrast", "sharpness", "saturation"]
        changes = {
            "brightness": (1.0, 1.2),
            "contrast": (1.0, 1.2),
            "sharpness": (1.0, 1.2),
            "saturation": (1.0, 1.2),
        }

    if denoise:
        img = img.filter(ImageFilter.MedianFilter(size=3))

    if grayscale:
        img = img.convert("L")

    img.save(output_path)

    return {
        "output_path": output_path,
        "enhanced": {
            "mode": "auto" if auto_enhance else "manual",
            "applied": applied,
            "changes": changes,
        },
    }
