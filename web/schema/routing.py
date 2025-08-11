from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class RoutingResponse(BaseModel):
# 사용자 정보
    question: str = Field(description="사용자 질문")
    response: str = Field(description="LLM 응답")
       
    isGuardpass: bool = Field(description="해당 시스템에 사용자 질문이 적합한지 판단한 결과")