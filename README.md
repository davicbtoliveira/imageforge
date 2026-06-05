# ImageForge

```
  .___                             ___________
  |   | _____ _____     ____   ____\_   _____/__________  ____   ____
  |   |/     \\__  \   / ___\_/ __ \|    __)/  _ \_  __ \/ ___\_/ __ \
  |   |  Y Y  \/ __ \_/ /_/  >  ___/|     \(  <_> )  | \/ /_/  >  ___/
  |___|__|_|  (____  /\___  / \___  >___  / \____/|__|  \___  / \___  >
            \/     \//_____/      \/    \/             /_____/      \/
```

> A Python CLI tool to resize, optimize, and enhance images — locally, fast, and without a GUI.

---

## Features

- **Resize** — by width, height, or scale factor with aspect ratio control
- **Optimize** — compress file size and convert between formats (JPEG, PNG, WebP)
- **Enhance** — adjust brightness, contrast, sharpness, saturation, denoise, and grayscale
- **Pipeline** — chain multiple operations in a single pass, saving only once
- **Info** — inspect image metadata, dimensions, and EXIF data

---

## Tech Stack

| Purpose          | Library  |
|------------------|----------|
| CLI interface    | `click`  |
| Image processing | `Pillow` |
| Testing          | `pytest` |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/davicbtoliveira/imageforge.git
cd imageforge
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install the package

```bash
pip install -e .
```

This installs ImageForge as a system command — you can now run `imageforge` from anywhere.

---

## Usage

### Resize

```bash
# Resize by width, keeping aspect ratio
imageforge resize photo.jpg --width 800

# Resize by height
imageforge resize photo.jpg --height 600

# Resize to exact dimensions
imageforge resize photo.jpg --width 1920 --height 1080 --no-keep-ratio

# Resize by scale factor (50%)
imageforge resize photo.jpg --scale 0.5

# Specify output path
imageforge resize photo.jpg --width 800 --output thumbnail.jpg
```

### Optimize

```bash
# Compress with quality setting
imageforge optimize photo.jpg --quality 80

# Convert to WebP
imageforge optimize photo.jpg --target-format webp --quality 85

# Strip metadata and save as progressive JPEG
imageforge optimize photo.jpg --strip-metadata --progressive

# Specify output path
imageforge optimize photo.jpg --quality 75 --output photo_compressed.jpg
```

### Enhance

```bash
# Auto enhance (smart defaults)
imageforge enhance photo.jpg --auto

# Manual adjustments
imageforge enhance photo.jpg --brightness 1.2 --contrast 1.3

# Sharpen and denoise
imageforge enhance photo.jpg --sharpness 2.0 --denoise

# Convert to grayscale
imageforge enhance photo.jpg --grayscale

# Specify output path
imageforge enhance photo.jpg --auto --output photo_enhanced.jpg
```

### Pipeline

Chain multiple operations in a single pass:

```bash
imageforge pipeline photo.jpg \
  --steps '[{"op":"resize","width":1280},{"op":"enhance","auto_enhance":true},{"op":"optimize","quality":80}]' \
  --output final.jpg
```

### Terminal UI

Launch the terminal UI workflow with `imageforge tui`. It supports the same resize, enhance, optimize, and pipeline operations, then prints a before -> after comparison with the input path, output path, and available diff metadata.

```bash
# Resize from the TUI workflow
imageforge tui photo.jpg --operation resize --width 800 --output thumbnail.jpg

# Enhance and compare before saving
imageforge tui photo.jpg \
  --operation enhance \
  --brightness 1.2 \
  --contrast 1.3 \
  --grayscale \
  --output photo_enhanced.jpg

# Optimize and convert format
imageforge tui photo.jpg \
  --operation optimize \
  --quality 80 \
  --target-format WEBP \
  --output photo.webp

# Run a multi-step pipeline
imageforge tui photo.jpg \
  --operation pipeline \
  --steps '[{"op":"resize","width":1280},{"op":"enhance","auto_enhance":true}]' \
  --output final.jpg
```

The comparison view always includes a terminal-safe text fallback:

```text
Before -> After
Before: photo.jpg
After: thumbnail.jpg
Dimensions: 1200x800 -> 800x533
```

---

## Project Structure

```
imageforge/
├── main.py                  # CLI entry point (Click commands)
├── editor/
│   ├── resize.py            # Resize logic
│   ├── optimize.py          # Compression & format conversion
│   ├── enhance.py           # Quality enhancements
│   ├── pipeline.py          # Chains multiple operations
│   └── tui.py               # Terminal UI workflow helpers
├── utils/
│   ├── file_handler.py      # Path validation, output naming
│   └── display.py           # Terminal colors and messages
├── tests/
│   ├── test_resize.py
│   ├── test_optimize.py
│   └── test_enhance.py
├── requirements.txt
├── setup.py
└── README.md
```

---

## Running Tests

```bash
pytest tests/
```

---

## Author

Feel free to open issues or suggest features.
