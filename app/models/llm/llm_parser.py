import os
from typing import List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.models.llm.mood_condition_schema import Mood, MoodConditionQuery, MoodInfo

load_dotenv()

# 1) LLM 인스턴스
llm = ChatOpenAI(
   model="gpt-4o-mini",
   temperature=0.0,
   openai_api_key=os.environ["OPENAI_API_KEY"] # API key 로딩
) 

# 2) LLM 출력 -> Pydantic 모델로 변환해주는 LangChain 컴포넌트
parser = PydanticOutputParser(pydantic_object=MoodConditionQuery)

# 3) 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_template(
   """
   너는 음악 추천을 위한 파라미터 추출기야.
   
   사용자의 한국어 문장을 읽고, 아래 JSON 스키마에 맞게 값을 채워줘
   
   - moods: 여러 개의 기분과 각각의 강도를 0~10 사이로 표현해줘
   - moods의 종류는 ["분노". "슬픔", "아픔", "불안", "창피", "기쁨", "사랑"] 이렇게 돼
   - condition: 상황(situation), 장소(place), 날씨(weather)를 각각 추출해줘
   - weather은 ["맑음", "폭염", "흐림", "비", "폭풍우", "눈"] 아래 중에서 골라서 써줘
   
   반드시 JSON형식만 출력하고, 설명 문장은 쓰지마
   {format_instructions}
   
   사용자 입력:
   {user_input}
   """
).partial(format_instructions=parser.get_format_instructions()) #TODO 이게 무슨 의미?

# 4) Langchain 구성: 프롬프트 -> LLM -> parser 순서대로 실행
chain = prompt | llm | parser if llm else None

_FALLBACK_MOODS = {
   "분노": Mood.anger,
   "슬픔": Mood.sadness,
   "아픔": Mood.pain,
   "불안": Mood.anxiety,
   "창피": Mood.shame,
   "기쁨": Mood.joy,
   "사랑": Mood.love
}

_FALLBACK_WEATHER = {
   "맑음": "sunny",
   "폭염": "hot",
   "흐림": "cloudy",
   "비": "rainy",
   "폭풍우": "storm",
   "눈": "snowy"
}

def _fallback_parse(user_input: str) -> MoodConditionQuery:
   moods: List[MoodInfo] = []
   
   for keyword, mood in _FALLBACK_MOODS.items():
      if keyword in user_input:
         moods.append(MoodInfo(mood=mood, mood_level=7)) #FIXME default=7?
         
   weather = None
   for keyword, value in _FALLBACK_WEATHER.items():
      if keyword in user_input:
         weather = value
         break #TODO 이게 뭐였더라

   return MoodConditionQuery.parse_obj(
      {
         "moods": moods,
         "condition": {
            "situation": None,
            "place": None,
            "weather": weather,
         },
      }
   )

def parse_user_input_to_query(user_input : str) -> MoodConditionQuery:
   """
   자연어 입력(user_input)을 받아서 Langchain으로 돌린 뒤, MoodConditionQuer(pydantic모델)로 변환해서 반환
   환경변수에 OPENAI_API_KEY가 없으면 간단한 키워드 매칭 기반으로 결과를 생성한다.
   """
   if chain:
      return chain.invoke({"user_input": user_input}) #TOOD 이게 뭐임?
   return _fallback_parse(user_input=)


if __name__ == "__main__":
   text = "비도 오고 우울해서 집에서 혼자 쉬고 싶어. 내일 출근하기 싫어"
   parsed = parse_user_input_to_query(text)
   print(parsed)
   print(parsed.model_dump())