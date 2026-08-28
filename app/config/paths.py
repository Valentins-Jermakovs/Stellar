# Path utilities for working with filesystem paths.
from pathlib import Path


# Root directory of the application.
# `__file__` points to this module, move two levels up
# to get the application base directory.
BASE_DIR = Path(__file__).resolve().parent.parent


# Directory containing the HTML templates used by the application.
TEMPLATES_DIR = BASE_DIR / "templates"