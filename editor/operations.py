from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from PIL import Image, ImageEnhance, ImageFilter

RESAMPLE_FILTERS = {
    "LANCZOS": Image.Resampling.LANCZOS,
    "BICUBIC": Image.Resampling.BICUBIC,
    "BILINEAR": Image.Resampling.BILINEAR,
    "NEAREST": Image.Resampling.NEAREST,
}


class Operation(ABC):
    @abstractmethod
    def apply(self, img: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
        ...


@dataclass
class ResizeOperation(Operation):
    width: int | None = None
    height: int | None = None
    scale: float | None = None
    keep_ratio: bool = True
    resample: str = "LANCZOS"

    def apply(self, img: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
        original_width, original_height = img.size
        original_ratio = original_width / original_height
        size = (self.width, self.height)

        filter_ = RESAMPLE_FILTERS.get(self.resample, Image.Resampling.LANCZOS)

        if self.scale is not None:
            new_h = int(original_height * self.scale)
            new_w = int(original_width * self.scale)
            img = img.resize((new_w, new_h), filter_)
        elif self.width is not None and self.height is not None:
            if self.keep_ratio:
                img.thumbnail(size, filter_)
            else:
                img = img.resize(size, filter_)
        elif self.width is not None and self.height is None:
            new_w = self.width
            if self.keep_ratio:
                new_h = int(self.width / original_ratio)
            else:
                new_h = original_height
            img = img.resize((new_w, new_h), filter_)
        elif self.height is not None and self.width is None:
            new_h = self.height
            if self.keep_ratio:
                new_w = int(self.height * original_ratio)
            else:
                new_w = original_width
            img = img.resize((new_w, new_h), filter_)
        else:
            raise ValueError("Must specify width, height, or scale")

        return img, {
            "dimensions": {"original": (original_width, original_height), "new": img.size},
        }


@dataclass
class EnhanceOperation(Operation):
    brightness: float = 1.0
    contrast: float = 1.0
    sharpness: float = 1.0
    saturation: float = 1.0
    auto_enhance: bool = False
    denoise: bool = False
    grayscale: bool = False

    def apply(self, img: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
        brightness = self.brightness
        contrast = self.contrast
        sharpness = self.sharpness
        saturation = self.saturation

        if self.auto_enhance:
            brightness, contrast, sharpness, saturation = 1.2, 1.2, 1.2, 1.2

        img = ImageEnhance.Brightness(img).enhance(brightness)
        img = ImageEnhance.Contrast(img).enhance(contrast)
        img = ImageEnhance.Sharpness(img).enhance(sharpness)
        img = ImageEnhance.Color(img).enhance(saturation)

        applied = []
        changes = {}

        if self.auto_enhance or brightness != 1.0:
            applied.append("brightness")
            changes["brightness"] = (1.0, brightness)
        if self.auto_enhance or contrast != 1.0:
            applied.append("contrast")
            changes["contrast"] = (1.0, contrast)
        if self.auto_enhance or sharpness != 1.0:
            applied.append("sharpness")
            changes["sharpness"] = (1.0, sharpness)
        if self.auto_enhance or saturation != 1.0:
            applied.append("saturation")
            changes["saturation"] = (1.0, saturation)

        if self.denoise:
            applied.append("denoise")
            changes["denoise"] = (False, True)
            img = img.filter(ImageFilter.MedianFilter(size=3))

        if self.grayscale:
            applied.append("grayscale")
            changes["grayscale"] = (False, True)
            img = img.convert("L")

        return img, {
            "enhanced": {
                "mode": "auto" if self.auto_enhance else "manual",
                "applied": applied,
                "changes": changes,
            },
        }


@dataclass
class OptimizeOperation(Operation):
    quality: int = 85
    target_format: str | None = None
    strip_metadata: bool = False
    progressive: bool = False

    def apply(self, img: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
        orig_format = (img.format or "JPEG").upper()
        output_format = (self.target_format or orig_format).upper()

        if output_format == "JPEG" and img.mode == "RGBA":
            img = img.convert("RGB")
        if self.strip_metadata:
            img = Image.frombytes(img.mode, img.size, img.tobytes())

        save_options = {}
        if self.target_format:
            save_options["format"] = output_format
        save_options["quality"] = self.quality
        save_options["progressive"] = self.progressive

        return img, {
            "format": {"original": orig_format, "new": output_format},
            "save_options": save_options,
        }
