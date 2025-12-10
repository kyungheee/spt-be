import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from mood_condition_schema import MoodConditionQuery

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
chain = prompt | llm | parser

def parse_user_input_to_query(user_input : str) -> MoodConditionQuery: #TODO 
   """
   자연어 입력(user_input)을 받아서 Langchain으로 돌린 뒤, MoodConditionQuery(pydantic모델)로 변환해서 반환
   """
   result: MoodConditionQuery = chain.invoke({"user_input": user_input})
   return result


if __name__ == "__main__":
   text = "비도 오고 우울해서 집에서 혼자 쉬고 싶어. 내일 출근하기 싫어"
   parsed = parse_user_input_to_query(text)
   print(parsed)
   print(parsed.model_dump())