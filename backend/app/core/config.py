"""Configuration settings for the application"""
import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "AI Pricing Monitor & Advisor"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    
    # N8N webhook configuration (to be used by Dev 4)
    n8n_webhook_url: str | None = None
    n8n_webhook_enabled: bool = False
    n8n_alert_email: str | None = None
    
    # LLM configuration (to be used by Dev 2)
    openai_api_key: str | None = None
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    
    # LangSmith / LangChain configuration (mapped from environment)
    langsmith_api_key: str | None = None
    langsmith_tracing: bool = False
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_project: str = "ride_flow"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Propagate LangSmith settings to standard LangChain environment variables
# This ensures LangChain's internal tracing mechanism picks them up automatically
if settings.langsmith_api_key:
    os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
    
    # Map tracing flag (v2 is the current standard)
    if settings.langsmith_tracing:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
    os.environ["LANGCHAIN_ENDPOINT"] = settings.langsmith_endpoint
    os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
