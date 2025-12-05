from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class Mood(str, Enum):
    anger = "분노"
    sadness = "슬픔"
    pain = "아픔"
    anxiety = "불안"
    shame = "창피"
    joy = "기쁨"
    love = "사랑"
    
class MoodInfo(BaseModel):
    mood: Mood = Field(default=None, description="기분 카테고리")
    mood_level: int = Field(default=0, ge=0, le=10, description = "기분의 강도(0~10)")

class Weather(str, Enum):
    sunny = "맑음"
    rainy = "비"
    cloudy = "흐림"
    snowy = "눈"
    # 번개, 폭풍우, 폭염 뭐 이런 것도 더 있겠지
    
class ConditionInput(BaseModel):
    """
    Lannchain에서 구조화 출력으로 받아온 결과를 FastAPI/백엔드에서 처리하기 위한 입력 형태
    """
    moods: List[MoodInfo] = Field(None, description = "감정 및 레벨 리스트")
    weather: Optional[Weather] = Optional(None, description = "날씨 정보, 없으면 None")
    situation: Optional[str] = Field(None, description="상황 설명 (공부, 퇴근길, 운동, 휴식 등)")
