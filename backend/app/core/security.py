from firebase_admin import auth
from fastapi import HTTPException, status

def verify_firebase_token(id_token: str) -> dict:
    """
    Verifies a Firebase ID token using the Firebase Admin SDK.
    Returns the decoded token dictionary if valid.
    Raises HTTPException if invalid or expired.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
