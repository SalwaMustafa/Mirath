from pydantic_settings import BaseSettings


class settings(BaseSettings):

    APP_NAME: str
    CONNECTION_URL: str
    DATABASE_NAME: str

    COHERE_API_KEY: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_MODEL_SIZE: int

    GEMINI_API_KEY: str
    GENERATION_MODEL_ID: str

    INPUT_DAFAULT_MAX_CHARACTERS: int
    GENERATION_DAFAULT_MAX_TOKENS: int
    GENERATION_DAFAULT_TEMPERATURE: float

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    
    class Config:
        env_file = ".env"


def get_settings():
    return settings()
