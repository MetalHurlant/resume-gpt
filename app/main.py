from fastapi import FastAPI
from pydantic import BaseModel
from app.openai_api import ChatApp
from app.db_api import SQLAPI
import uuid

from . import config

settings = config.Settings()

app = FastAPI()
my_gpt = ChatApp(settings.openai)
db_api = SQLAPI(settings.database)


@app.get("/")
async def root():
    return {
        "response": "Hello there"
    }

if settings.environment == "dev":
    @app.get("/settings")
    async def get_settings():
        return settings.dict()


class Message(BaseModel):
    session_id: str | None
    message: str


@app.get("/messages")
async def getMessage(session_id: str) -> dict:
    messages = db_api.get_messages(session_id=session_id)
    messages = sorted(messages, key=lambda m: m["message_id"])

    return {"response": messages}


@app.post("/messages")
async def postMessage(message: Message) -> dict:
    if not message.session_id:
        message.session_id = str(uuid.uuid4())

    db_api.post_message(message.session_id, message.message, "user")
    messages = db_api.get_messages(session_id=message.session_id)
    messages = sorted(messages, key=lambda m: m["message_id"])

    bot_response = my_gpt.chat(messages)

    db_api.post_message(message.session_id, bot_response, "assistant")
    messages = db_api.get_messages(session_id=message.session_id)
    messages = sorted(messages, key=lambda m: m["message_id"])

    return {"response": messages}
