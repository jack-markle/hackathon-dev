"""Configuration settings for the application"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "AI Pricing Monitor & Advisor"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    
    # N8N webhook configuration (to be used by Dev 4)
    n8n_webhook_url: str | None = None
    n8n_enabled: bool = False
    
    # LLM configuration (to be used by Dev 2)
    openai_api_key: str | None = None
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

