import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List
from ai.config import config
from app.modules.severity.models import PriorityEnum

client = genai.Client(api_key=config.gemini_api_key) if config.gemini_api_key else None

class SeverityResult(BaseModel):
    priority: PriorityEnum
    severity_score: int = Field(ge=0, le=100)
    severity_reasons: List[str]

def assess_severity(category: str, description: str, address: str) -> dict:
    """
    Generates severity score via Gemini, enforcing JSON schema.
    Also applies deterministic guardrails.
    """
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "severity_prompt.txt")
    with open(prompt_path, "r") as f:
        system_prompt = f.read()
        
    content = f"Category: {category}\nDescription: {description}\nLocation Context: {address}"
    
    # 1. Deterministic Guardrails
    description_lower = description.lower()
    if "fatality" in description_lower or "major accident" in description_lower or "collapsed" in description_lower:
        base_priority = "P0"
    elif "trapped" in description_lower or "fire" in description_lower:
        base_priority = "P1"
    else:
        base_priority = None
        
    try:
        response = client.models.generate_content(
            model=config.model_name,
            contents=content,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=SeverityResult,
                temperature=0.1
            )
        )
        result = json.loads(response.text)
        
        priority = result.get("priority", "P3")
        
        # Apply guardrails
        if base_priority == "P0":
            priority = "P0"
        elif base_priority == "P1" and priority in ["P2", "P3"]:
            priority = "P1"
            
        return {
            "priority": priority,
            "severity_score": int(result.get("severity_score", 0)),
            "severity_reasons": result.get("severity_reasons", []),
            "model_provider": "google",
            "model_name": config.model_name
        }
    except Exception as e:
        # Fallback
        return {
            "priority": base_priority or "P2", # Safe fallback
            "severity_score": 50,
            "severity_reasons": [f"Parsing error: {str(e)}", "fallback_applied"],
            "model_provider": "google",
            "model_name": config.model_name
        }
