from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.chat import router as chat_router
from app.models.llm.llm_parser import parse_user_input_to_query
from app.models.llm.mood_condition_schema import MoodConditionQuery

app = FastAPI()

# CORS: 프론트 레포에서 백엔드로 요청 보낼 수 있게 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 우선 전체 허용, 나중에 도메인 좁히면 됨
    allow_credentials=True,
    allow_method=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    prompt: str
    
@app.post("/llm", response_model=MoodConditionQuery)
async def llm_endpoint(data: Prompt):
    """
    프론트에서 자연어 프롬프트를 받으면
    LLM 파서에 넘겨서 MoodConditionQuery로 변환해 반환
    """
    result = parse_user_input_to_query(data.prompt)
    return result

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.fromtimestamp(0, timezone.utc).isoformat()}

app.include_router(chat_router)