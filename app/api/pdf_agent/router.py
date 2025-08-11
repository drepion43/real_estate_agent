import os
import json

from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage, AIMessage

from .schema import PDFAgentState, PDFAgentRouterScheme
from .service import PDFAgent
from api.utils import parse_messages


router = APIRouter(prefix="/pdf_agent")


@router.post("/invoke")
def pdf_agent_router(
    scheme: PDFAgentRouterScheme,
    request: Request,
) -> PDFAgentRouterScheme:
    agent = request.app.pdf_agent
    messages = parse_messages(scheme.state)
    scheme.state["messages"] = messages
    state = PDFAgentState(**scheme.state)

    out_state = agent.workflow.invoke(state, scheme.config)
    scheme.state = out_state
    return scheme


@router.post("/ainvoke")
async def pdf_agent_router(
    scheme: PDFAgentRouterScheme,
    request: Request,
) -> PDFAgentRouterScheme:
    agent: PDFAgent = request.app.pdf_agent
    messages = parse_messages(scheme.state)
    scheme.state["messages"] = messages
    state = PDFAgentState(**scheme.state)

    out_state = await agent.workflow.ainvoke(state, scheme.config)
    scheme.state = out_state
    return scheme


@router.post("/vectorize")
def pdf_agent_vectorize_router(
    scheme: PDFAgentRouterScheme,
    request: Request,
) -> PDFAgentRouterScheme:
    agent: PDFAgent = request.app.pdf_agent
    out_state = agent.vectorize(scheme.state, scheme.config)
    scheme.state = out_state
    return scheme


@router.post("/avectorize")
async def pdf_agent_vectorize_router(
    scheme: PDFAgentRouterScheme,
    request: Request,
) -> PDFAgentRouterScheme:
    agent: PDFAgent = request.app.pdf_agent
    out_state = await agent.avectorize(scheme.state, scheme.config)
    scheme.state = out_state
    return scheme


@router.post("/uploadfiles")
async def create_upload_files(file: UploadFile):
    filename = os.path.join("pdf_assets", file.filename)
    with open(filename, 'wb') as f:
        f.write(await file.read())


async def async_generator(
    scheme: PDFAgentRouterScheme,
    request: Request,
):
    agent: PDFAgent = request.app.pdf_agent
    resp = agent.workflow.astream_events(scheme.state, scheme.config, version="v2")
    async for event in resp:
        if event["event"] == "on_chat_model_stream":
            content = event["data"]["chunk"].content
        else:
            content = ""

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
            "config": scheme.config,
            "tool_inputs": tool_inputs,
        }

        output = json.dumps(output, ensure_ascii=False) + "\n"
        yield output


@router.post("/astream")
async def pdf_agent_stream(scheme: PDFAgentRouterScheme, request: Request):
    messages = parse_messages(scheme.state)
    scheme.state["messages"] = messages
    state = PDFAgentState(**scheme.state)
    scheme.state = state

    return StreamingResponse(
        async_generator(scheme, request),
        media_type="text/event-stream",
    )
