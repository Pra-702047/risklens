import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class AIConfig(BaseSettings):
    gemini_api_key: str = ""
    auto_accept_threshold: float = 0.80
    review_threshold: float = 0.60
    model_name: str = "gemini-2.5-flash"
    embedding_model_name: str = "text-embedding-004"
    
    duplicate_geo_radius_meters: float = 500.0
    duplicate_time_window_hours: int = 72
    duplicate_similarity_auto_link: float = 0.90
    duplicate_similarity_review: float = 0.75

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../backend/.env"),
        env_file_encoding='utf-8',
        extra='ignore'
    )

config = AIConfig()
