from pydantic_settings import BaseSettings
from typing import List


class settings(BaseSettings):

    APP_NAME: str
    CONNECTION_URL: str
    DATABASE_NAME: str

    COHERE_API_KEY: str

    EMBEDDING_MODEL_ID_LITERAL: List[str] = None
    EMBEDDING_MODEL_ID: str
    EMBEDDING_MODEL_SIZE: int

    GENERATION_MODEL_ID_LITERAL: List[str] = None
    GEMINI_API_KEY: str
    GENERATION_MODEL_ID: str

    INPUT_DAFAULT_MAX_CHARACTERS: int
    GENERATION_DAFAULT_MAX_TOKENS: int
    GENERATION_DAFAULT_TEMPERATURE: float

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    QDRANT_URL: str
    DISTANCE_METHOD: str
    VECTOR_DB_BACKEND: str

    TAVILY_API_KEY: str

    PRIMARY_LANG: str
    DEFAULT_LANG: str
    
    GROQ_API_KEY: str
    TRANSCRIPTION_MODEL_ID: str

    PADDLE_OCR_URL: str
    PADDLE_OCR_TOKEN: str

    AUDIO_MAX_SIZE: int

    IMAGE_ALLOWED_TYPES: List[str]
    IMAGE_MAX_SIZE: int 

    class Config:
        env_file = ".env"


def get_settings():
    return settings()
