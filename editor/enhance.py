from PIL import Image, ImageEnhance, ImageFilter


def process_enhance(
    img: Image.Image,
    brightness: float,
    contrast: float,
    sharpness: float,
    saturation: float,
    auto_enhance: bool,
    denoise: bool,
    grayscale: bool,
) -> tuple[Image.Image, dict]:
    if auto_enhance:
        brightness, contrast, sharpness, saturation = 1.2, 1.2, 1.2, 1.2

    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    img = ImageEnhance.Color(img).enhance(saturation)

    applied = []
    changes = {}

    if auto_enhance or brightness != 1.0:
        applied.append("brightness")
        changes["brightness"] = (1.0, brightness)
    if auto_enhance or contrast != 1.0:
        applied.append("contrast")
        changes["contrast"] = (1.0, contrast)
    if auto_enhance or sharpness != 1.0:
        applied.append("sharpness")
        changes["sharpness"] = (1.0, sharpness)
    if auto_enhance or saturation != 1.0:
        applied.append("saturation")
        changes["saturation"] = (1.0, saturation)

    if denoise:
        applied.append("denoise")
        changes["denoise"] = (False, True)
        img = img.filter(ImageFilter.MedianFilter(size=3))

    if grayscale:
        applied.append("grayscale")
        changes["grayscale"] = (False, True)
        img = img.convert("L")

    return img, {
        "enhanced": {
            "mode": "auto" if auto_enhance else "manual",
            "applied": applied,
            "changes": changes,
        },
    }
