import os

# ===============================
# Project Directories
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

# ===============================
# AI Models
# ===============================

TROCR_MODEL = "microsoft/trocr-base-handwritten"

# ===============================
# Image Settings
# ===============================

IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 1600

# ===============================
# OCR Settings
# ===============================

LANGUAGE = "eng"

# ===============================
# Output Formats
# ===============================

SUPPORTED_FORMATS = [
    "txt",
    "pdf",
    "docx"
]