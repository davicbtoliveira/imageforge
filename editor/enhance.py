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
    grayscale: bool
) -> str:
    if auto_enhance:
        brightness, contrast, sharpness, saturation = 1.2, 1.2, 1.2, 1.2

    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    img = ImageEnhance.Color(img).enhance(saturation)

    if denoise:
        img = img.filter(ImageFilter.MedianFilter(size=3))

    if grayscale:
        img = img.convert("L")

    img.save(output_path)
    return output_path
