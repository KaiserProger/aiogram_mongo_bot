from pydantic import BaseSettings


class Config(BaseSettings):
    token: str
    mongo_host: str
    mongo_user: str
    mongo_password: str
