import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

from PIL import Image

from shared.result import OperationResult


class ImageWriter(ABC):
    @abstractmethod
    def save(
        self,
        img: Image.Image,
        output_path: str,
        fmt: str | None = None,
        quality: int = 85,
        progressive: bool = False,
    ) -> OperationResult:
        ...


@dataclass
class FileSystemWriter(ImageWriter):
    def save(
        self,
        img: Image.Image,
        output_path: str,
        fmt: str | None = None,
        quality: int = 85,
        progressive: bool = False,
    ) -> OperationResult:
        save_kwargs = {}
        if fmt is not None:
            save_kwargs["format"] = fmt
        save_kwargs["quality"] = quality
        save_kwargs["progressive"] = progressive

        try:
            img.save(output_path, **save_kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to save image {e}")

        return OperationResult(
            output_path=output_path,
            input_path=output_path,
            changes={"size": {"new": os.path.getsize(output_path)}},
        )
