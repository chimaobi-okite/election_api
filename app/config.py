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
    algorithm: str
    access_token_expire_minutes: int
    cloud_api_key:str
    cloud_api_secret:str
    cloud_api_name:str

    class Config:
        env_file = ".env"


settings = Settings()