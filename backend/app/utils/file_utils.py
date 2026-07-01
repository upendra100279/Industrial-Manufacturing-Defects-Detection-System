"""
Helpers for saving uploaded files to disk with unique, collision-safe names.
"""
import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "storage/uploads"
PROCESSED_DIR = "storage/processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


def save_upload_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1] or ".jpg"
    unique_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, unique_name)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    return path


def build_processed_path(original_path: str) -> str:
    filename = os.path.basename(original_path)
    return os.path.join(PROCESSED_DIR, f"processed_{filename}")
