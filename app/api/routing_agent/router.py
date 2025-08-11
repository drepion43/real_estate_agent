import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage, AIMessage
from .service import RoutingAgent
from .schema import RoutingAgentState, RoutingAgentRouterScheme
from api.utils import parse_messages  # 기존에 사용한 메시지 변환 함수 재활용

router = APIRouter(prefix="/routing_agent")


@router.post("/invoke")
def routing_agent_invoke(
    scheme: RoutingAgentRouterScheme,
    request: Request,
) -> RoutingAgentRouterScheme:
    """
    RoutingAgent 의 동기 함수 엔드포인트
    """
    agent: RoutingAgent = request.app.routing_agent

    result = agent.agent_workflow.invoke(scheme, scheme.config)
    return result


@router.post("/ainvoke")
async def routing_agent_ainvoke(
    scheme: RoutingAgentRouterScheme,
    request: Request,
) -> RoutingAgentRouterScheme:
    """
    RoutingAgent 의 비동기 함수 엔드포인트
    """
    agent: RoutingAgent = request.app.routing_agent
        
    result = await agent.agent_workflow.ainvoke(scheme, scheme.config)
    return result
