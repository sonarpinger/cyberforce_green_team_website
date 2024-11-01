from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: SecretStr
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_NAME: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()