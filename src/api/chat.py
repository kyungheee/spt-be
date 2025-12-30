from datetime import datetime
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.models.llm.llm_parser import parse_user_input_to_query
from src.models.llm.mood_condition_schema import MoodConditionQuery

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatMessage(BaseModel):
    content: str = Field(..., description= "사용자 입력 메세지")

class BotMessage(BaseModel):
    id: str
    type: Literal["bot"]