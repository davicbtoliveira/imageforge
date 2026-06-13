from dataclasses import dataclass, field
from typing import Any


@dataclass
class OperationResult:
    output_path: str
    input_path: str
    changes: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineResult:
    output_path: str
    steps: list[OperationResult]
