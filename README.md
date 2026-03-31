# ImageForge

> A Python CLI tool to resize, optimize, and enhance images — locally, fast, and without a GUI.

---

## What is it?

ImageForge is a command-line image processing tool built in Python. It lets you manipulate images directly from your terminal — no internet connection, no third-party service, no graphical interface needed.

**What it does:**
- **Resize** images by fixed dimensions or a percentage scale factor
- **Optimize** images by compressing file size and converting formats (JPEG, PNG, WebP)
- **Enhance** image quality by adjusting brightness, contrast, sharpness, and saturation
- **Inspect** image metadata (dimensions, format, file size, EXIF data)
- **Pipeline** multiple operations in a single command pass

---

## Project Status

> 🚧 **In development** — core utilities are done, editor modules are in progress.

| Module               | Status        |
|----------------------|---------------|
| `utils/display.py`   | ✅ Done        |
| `utils/file_handler.py` | ✅ Done     |
| `editor/resize.py`   | 🔄 In progress |
| `editor/optimize.py` | 🔄 In progress |
| `editor/enhance.py`  | 🔄 In progress |
| `editor/pipeline.py` | ⏳ Pending     |
| `tests/`             | ⏳ Pending     |

---

## Tech Stack

| Purpose            | Library     |
|--------------------|-------------|
| CLI interface      | `click`     |
| Image processing   | `Pillow`    |
| Testing            | `pytest`    |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/imageforge.git
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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the tool

```bash
python main.py --help
```

---

## Usage (planned)

Once fully implemented, commands will follow this pattern:

```bash
# Resize by width, keeping aspect ratio
python main.py resize photo.jpg --width 800

# Optimize and convert to WebP
python main.py optimize photo.jpg --quality 80 --format webp

# Enhance with automatic settings
python main.py enhance photo.jpg --auto

# View image metadata
python main.py info photo.jpg

# Run a pipeline of operations in one pass
python main.py pipeline photo.jpg --steps '[{"op":"resize","width":1280},{"op":"optimize","quality":85}]'
```

---

## Project Structure

```
imageforge/
├── main.py                  # CLI entry point
├── editor/
│   ├── resize.py            # Resize logic
│   ├── optimize.py          # Compression & format conversion
│   ├── enhance.py           # Quality enhancements
│   └── pipeline.py          # Chains multiple operations
├── utils/
│   ├── file_handler.py      # Path validation, output naming
│   └── display.py           # Terminal colors and messages
├── tests/
├── requirements.txt
└── README.md
```

---

