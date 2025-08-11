from fastapi import APIRouter, Request

from langchain_core.messages import HumanMessage, AIMessage

from .schema import BaseAgentState, BaseAgentRouterScheme
from api.utils import parse_messages


router = APIRouter(prefix="/base_agent")


@router.post("/invoke")
def base_agent_router(
    scheme: BaseAgentRouterScheme,
    request: Request,
) -> BaseAgentRouterScheme:
    agent = request.app.base_agent
    messages = parse_messages(scheme.state)
    scheme.state["messages"] = messages
    state = BaseAgentState(**scheme.state)

    out_state = agent.workflow.invoke(state, scheme.config)
    scheme.state = out_state
    return scheme


@router.post("/ainvoke")
async def base_agent_router(
    scheme: BaseAgentRouterScheme,
    request: Request,
) -> BaseAgentRouterScheme:
    agent = request.app.base_agent
    messages = parse_messages(scheme.state)
    scheme.state["messages"] = messages
    state = BaseAgentState(**scheme.state)

    out_state = await agent.workflow.ainvoke(state, scheme.config)
    scheme.state = out_state
    return scheme


