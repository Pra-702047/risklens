import json
from google import genai
from ai.config import config

client = genai.Client(api_key=config.gemini_api_key) if config.gemini_api_key else None

def generate_embedding(text: str) -> list[float]:
    """
    Generates a dense vector embedding using Gemini's embedding model.
    Falls back to a zero vector if the API key is missing or an error occurs.
    """
    if not client:
        return [0.0] * 768
        
    try:
        response = client.models.embed_content(
            model=config.embedding_model_name,
            contents=text
        )
        # The response object has an embeddings property
        if hasattr(response, 'embeddings') and len(response.embeddings) > 0:
            return response.embeddings[0].values
        
        # Fallback to dictionary access just in case
        return response[0]['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return [0.0] * 768
