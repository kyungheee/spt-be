from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from parsing_schemas import MusicQuery


# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_template(
   """
   너는 음악 추천을 위한 파라미터 추출기야.
   사용자의 한국어 문장을 읽고, 아래 JSON 스키마에 맞게 값을 채워줘
   
   반드시 JSON형식만 출력하고, 설명 문장은 쓰지마
   {format_instructions}
   
   사용자 입력:
   {user_input}
   """
)

# LLM
llm = ChatOpenAI(
   model="gpt-4o-mini",
   temperature=0.0
)

# 출력 파서
parser = PydanticOutputParser(pydantic_object=MusicQuery)   

# 체인 구성
chain = prompt | llm | parser

def parse_user_input_to_query(user_input : str) -> MusicQuery:
   """
   자연어 -> MuicQuery(pydantic 모델)로 변환
   """
   _prompt = prompt.format(
      user_input = user_input,
      format_instructions = parser.get_format_instructions()
   )
   result: MusicQuery = parser.parse(
      llm.invoke(_prompt).content
   )
   return result