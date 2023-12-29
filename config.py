import os

# from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings:
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGODB_NAME: str = os.getenv("MONGODB_NAME")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE")
    PORT: int = 8000
    HOST: str = "0.0.0.0"


settings = Settings()
