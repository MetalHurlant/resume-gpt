import os
import shutil
from pydantic import BaseModel, BaseSettings

class Database(BaseModel):
    file_path: str

class OpenAI(BaseModel):
    api_key: str
    chat_completion_model: str

class Settings(BaseSettings):
    database: Database
    openai: OpenAI

    class Config:
        env_nested_delimiter = "__"
        env_file = ".env"
        if not os.path.isfile(env_file):
            shutil.copy(f"{env_file}.dist", env_file)