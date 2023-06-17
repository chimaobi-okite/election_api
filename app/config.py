import os
from pydantic import BaseSettings


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_DIR = os.path.join(ROOT_DIR, "photos")


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    review_after:int
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()