from typing import TypedDict
from pydantic import BaseModel, Field

class RoutingAgentState(TypedDict):
    # 사용자 정보
    question: str = Field(description="사용자 질문")
    response: str = Field(description="LLM 응답")
       
    isGuardpass: bool = Field(description="해당 시스템에 사용자 질문이 적합한지 판단한 결과")
    # pdf_info: list[str] = Field(description="현재 존재하는 PDF 파일 이름들")

class BaseConfig(TypedDict):
    thread_id: str
    user_id: str
    
class RoutingAgentConfig(TypedDict):
    config: dict = Field(description="설정 정보")
    # pdf_path: list[str] = Field(description="PDF 파일 경로")
    configurable: BaseConfig

    
class RoutingAgentRouterScheme(BaseModel):
    state: RoutingAgentState
    config: RoutingAgentConfig
