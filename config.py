from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Folder containing the mock PDFs
PDF_DIR = BASE_DIR / "Mock PDF Documents"

# Automatically load all PDFs
PDF_PATHS = list(PDF_DIR.glob("*.pdf"))

DATABASE_NAME = "documents.db"