import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException, status
from pathlib import Path

# MVP Local Storage Directory
if os.environ.get("VERCEL"):
    UPLOAD_DIR = Path("/tmp/uploads/evidence")
else:
    UPLOAD_DIR = Path("uploads/evidence")
    
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "video/mp4",
    "audio/mpeg",
    "audio/mp4"
}
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

async def save_evidence(file: UploadFile) -> str:
    """
    Validates and saves an uploaded file to local storage.
    Returns the public URL (or local path for MVP).
    """
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    
    # Read file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB"
        )
    
    # Secure filename generation
    ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    secure_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = UPLOAD_DIR / secure_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # In a real app, return S3 URL or similar. For MVP, return the static path.
    return f"/static/uploads/evidence/{secure_filename}"
