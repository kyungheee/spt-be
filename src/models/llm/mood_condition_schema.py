from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

# ---------------------------
# 1. Mood(기분/기분의 강도) 정의
# ---------------------------
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

# ---------------------------
# 2. Condition(상황/장소/날씨) 정의
# ---------------------------
class Weather(str, Enum):
    sunny = "맑음"
    hot = "폭염"
    cloudy = "흐림"
    rainy = "비"
    storm = "폭풍우"
    snowy = "눈"
    
class Condition(BaseModel):   
    situation: Optional[str] = Field(default=None, description="현재 상황 (공부, 퇴근길, 운동, 휴식 등)")
    place: Optional[str] = Field(default=None, description="현재 장소 (집, 카페, 지하철, 헬스장 등)")
    weather: Optional[str] = Field(default=None, description="날씨 정보")

# ---------------------------
# 3. 최종 스키마: Mood + Condition 묶음
# ---------------------------    
class MoodConditionQuery(BaseModel):
    """LLM이 출력하는 최종 구조화 결과"""    
    moods: List[MoodInfo] = Field(default_factory=list, description="기분과 기분 강도")
    condition: Condition = Field(default_factory=Condition, description="상황/장소/날씨 정보")