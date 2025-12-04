from pydantic import BaseModel, Field, field_validator
from typing import List, Optional 

class MusicQuery(BaseModel):
   mood: Optional[str] = Field(default=None, description="사용자의 기분 (예: happy, sad, calm 등)")
   situation: Optional[str] = Field(default=None, description = "듣는 상황 (예: study, workdout, sleep 등)")
   weather: Optional[str] = Field(default=None, description="날씨 (예: rainy, sunnym cloudy 등)")
   energy: Optional[str] = Field(default=None, description="에너지 레벨 (예: low, medium, high)")
   # genres: Optional[list[str]] = Field(default=None,description="사용자가 언급한 또는 선호하는 장르 리스트 (예: indie, acoustic)")
   limit: int = Field(default=10, description = "추천 곡 개수, 기본값 10")
   
   @field_validator("genres", mode="before")
   @classmethod
   def ensure_list(cls, v):
      # 아무것도 없으면 그대로
      if v is None:
         return None
      if not isinstance(v, (list, str)):
         v = str(v)
      # "indie" 같이 문자열 하나면 ["indie"]로 변환
      if isinstance(v, str):
         return [v]
      # 이미 리스트면 그대로
      return [str(item) for item in v]
   
# if __name__ == "__main__":
#    print(MusicQuery(genres="indie").genres)
#    print(MusicQuery(genres=["indie", "acoustic"]).genres)
#    print(MusicQuery(genres=None).genres)