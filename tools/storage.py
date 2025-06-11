# tools/storage.py
import os
import uuid
from pathlib import Path

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


def save_uploaded_file(uploaded_file):
    file_ext = os.path.splitext(uploaded_file.name)[-1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# This function saves an uploaded file to the uploads directory.
# It generates a unique filename using UUID and returns the path to the saved file.