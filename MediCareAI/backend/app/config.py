import os
from dataclasses import dataclass
@dataclass(frozen=True)
class Settings:
    secret_key:str=os.getenv('SECRET_KEY','change-me-in-production'); access_token_minutes:int=int(os.getenv('ACCESS_TOKEN_MINUTES','1440')); ai_api_key:str=os.getenv('AI_API_KEY',''); ai_api_base_url:str=os.getenv('AI_API_BASE_URL','https://api.openai.com/v1'); ai_model:str=os.getenv('AI_MODEL','gpt-4o-mini'); cors_origins:str=os.getenv('CORS_ORIGINS','http://localhost:8081,http://localhost:19006')
settings=Settings()
