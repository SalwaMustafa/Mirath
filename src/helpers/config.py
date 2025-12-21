from pydantic_settings import BaseSettings


class settings(BaseSettings):

    APP_NAME: str
    CONNECTION_URL: str
    DATABASE_NAME: str

    
    class Config:
        env_file = ".env"


def get_settings():
    return settings()
