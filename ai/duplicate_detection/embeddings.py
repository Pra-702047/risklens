import json
from google import genai
from ai.config import config

client = genai.Client(api_key=config.gemini_api_key) if config.gemini_api_key else None

def generate_embedding(text: str) -> list[float]:
    """
    Generates a dense vector embedding using Gemini's embedding model.
    """
    response = client.models.embed_content(
        model=config.embedding_model_name,
        contents=text
    )
    # The response object has an embeddings property
    # According to genai SDK, response.embeddings[0].values
    # Or response.embeddings[0] depending on SDK version.
    
    # We will try the standard structure
    if hasattr(response, 'embeddings') and len(response.embeddings) > 0:
        return response.embeddings[0].values
    
    # Fallback to dictionary access just in case
    return response[0]['embedding']
