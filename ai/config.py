import os
from pydantic_settings import BaseSettings

class AIConfig(BaseSettings):
    gemini_api_key: str = os.getenv("GEMINI_API_KEY") or ""
    auto_accept_threshold: float = float(os.getenv("AI_AUTO_ACCEPT_THRESHOLD") or "0.80")
    review_threshold: float = float(os.getenv("AI_REVIEW_THRESHOLD") or "0.60")
    model_name: str = "gemini-2.5-flash"
    embedding_model_name: str = "text-embedding-004"
    
    duplicate_geo_radius_meters: float = float(os.getenv("DUPLICATE_GEO_RADIUS_METERS") or "500")
    duplicate_time_window_hours: int = int(os.getenv("DUPLICATE_TIME_WINDOW_HOURS") or "72")
    duplicate_similarity_auto_link: float = float(os.getenv("DUPLICATE_SIMILARITY_AUTO_LINK") or "0.90")
    duplicate_similarity_review: float = float(os.getenv("DUPLICATE_SIMILARITY_REVIEW") or "0.75")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

config = AIConfig()
