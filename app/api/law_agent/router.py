import json
import os

from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage, AIMessage

from .service import LawAgent
from .schema import LawAgentState, LawAgentRouterScheme
from api.utils import parse_messages


router = APIRouter(prefix="/law_agent")

@router.post("/uploadfiles")
async def create_upload_files(file: UploadFile):
    filename = os.path.join("pdf_assets", file.filename)
    with open(filename, 'wb') as f:
        f.write(await file.read())

@router.post("/invoke")
def law_agent_invoke(
    scheme: LawAgentRouterScheme,
    request: Request
) -> LawAgentRouterScheme:
    agent: LawAgent = request.app.law_agent
    messages = parse_messages(scheme.state)
    scheme.state["messages"] = messages
    state = LawAgentState(**scheme.state)

    out_state = agent.workflow.invoke(state, scheme.config)
    scheme.state = out_state
    return scheme

@router.post("/ainvoke")
async def law_agent_ainvoke(
    scheme: LawAgentRouterScheme,
    request: Request
) -> LawAgentRouterScheme:
    agent: LawAgent = request.app.law_agent
    messages = parse_messages(scheme.state)
    scheme.state["messages"] = messages
    state = LawAgentState(**scheme.state)

    out_state = await agent.workflow.ainvoke(state, scheme.config)
    scheme.state = out_state
    return scheme


@router.post("/astream")
async def law_agent_stream(
    scheme: LawAgentRouterScheme,
    request: Request
):
    agent: LawAgent = request.app.law_agent
    messages = parse_messages(scheme.state)
    scheme.state["messages"] = messages
    state = LawAgentState(**scheme.state)
    async def async_gen():
        resp = agent.workflow.astream_events(state, scheme.config, version="v2")
        async for event in resp:
            tags = event.get("tags", None)

            if tags and "Summary" in tags: continue      # Summary tags에 대해선 따로 content를 Client에 Send하지 않음.

            # Chat Model의 답변 처리
            if event["event"] == "on_chat_model_stream":
                content = event["data"]["chunk"].content
            else:
                content = ""

            # CrawlTool의 입력 변수
            if event["event"] == "on_tool_start":
                tool_inputs = event["data"]["input"]
            else:
                tool_inputs = None

            output = {
                "content": content,
                "event": {
                    "state": event["event"],
                    "name": event["name"],
                },
                "tags": tags,
                "config": scheme.config,
                "tool_inputs": tool_inputs,
            }

            output = json.dumps(output, ensure_ascii=False) + "\n"
            yield output

    return StreamingResponse(async_gen(), media_type="text/event-stream")
