import sys
import os

# Add root project path so we can import the top-level ai/ module
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from ai.gateway import analyze_complaint

def get_ai_classification(description: str, file_urls: list = None) -> dict:
    """
    Wrapper around the core AI module.
    Returns: {
        "predicted_category": str,
        "subcategory": str,
        "confidence": float,
        "reason_codes": list,
        "model_provider": str,
        "model": str,
        "model_version": str
    }
    """
    return analyze_complaint(description, file_urls)
