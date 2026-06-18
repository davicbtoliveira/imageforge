# ImageForge Domain Model

## Core Concepts

- **Image** — A PIL Image object being processed. Flows through a sequence of operations.
- **Operation** — A single image transformation (resize, enhance, optimize). Each operation is a typed dataclass that implements `apply(img) -> (img, metadata)`.
- **Pipeline** — A sequence of Operations applied in order. The result of each step feeds the next.
- **ImageWriter** — An adapter that persists an image to a destination (filesystem, in-memory, etc.).
- **OperationResult** — Data about what changed after applying an Operation.
- **PipelineResult** — The combined results of all steps in a Pipeline.
