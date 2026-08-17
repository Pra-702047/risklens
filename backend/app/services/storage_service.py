import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException, status
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError

# S3 Configuration
USE_S3 = os.environ.get("USE_S3", "False").lower() in ("true", "1", "t")
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME", "risklens-evidence")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

if USE_S3:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_REGION
    )

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
    Validates and saves an uploaded file to S3 (if enabled) or local storage.
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
            detail=f"File too large. Max size is {MAX_FILE_SIZE_MB}MB."
        )
        
    ext = file.filename.split(".")[-1] if file.filename else "bin"
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    
    if USE_S3:
        try:
            # Upload to S3
            s3_client.upload_fileobj(
                file.file,
                AWS_BUCKET_NAME,
                new_filename,
                ExtraArgs={"ContentType": file.content_type, "ACL": "public-read"}
            )
            # Return the public S3 URL
            return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{new_filename}"
        except NoCredentialsError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="S3 credentials not available"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload to S3: {str(e)}"
            )
    else:
        # Local Storage Fallback
        file_path = UPLOAD_DIR / new_filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # In MVP, this relies on a StaticFiles mount returning the file
        return f"/uploads/evidence/{new_filename}"
