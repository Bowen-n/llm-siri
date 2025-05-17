from enum import Enum

from pydantic import BaseModel, Field


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    role: str
    content: str


class Response(BaseModel):
    think: str
    response: str


class ChatMessage(BaseModel):
    messages: list[Message]
    response: Response
