import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List
from ai.config import config

# We need to construct the client.
# Note: Google GenAI uses `genai.Client(api_key=...)`
client = genai.Client(api_key=config.gemini_api_key) if config.gemini_api_key else None

class ClassificationResult(BaseModel):
    category: str
    subcategory: str
    confidence: float
    reason_codes: List[str]

def classify_text(text: str) -> dict:
    if not client:
        raise ValueError("GEMINI_API_KEY is missing from environment. Cannot perform AI analysis.")

    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "classification_prompt.txt")
    with open(prompt_path, "r") as f:
        system_prompt = f.read()
        
    try:
        # We enforce structured JSON response via the SDK
        response = client.models.generate_content(
            model=config.model_name,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=ClassificationResult,
                temperature=0.1
            )
        )
        
        result = json.loads(response.text)
        return {
            "predicted_category": result.get("category", "OTHER"),
            "subcategory": result.get("subcategory", "unknown"),
            "confidence": float(result.get("confidence", 0.0)),
            "reason_codes": result.get("reason_codes", []),
            "model_provider": "google",
            "model": config.model_name,
            "model_version": "latest" # Could be pinned version
        }
    except Exception as e:
        raise ValueError(f"AI API call failed: {str(e)}")
