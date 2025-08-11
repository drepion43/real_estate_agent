import os

from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI

from langgraph.checkpoint.memory import MemorySaver

from api.base_agent.service import BaseAgent
from api.applyhome_agent.service import ApplyhomeAgent
from api.pdf_agent.service import PDFAgent
from api.routing_agent.service import RoutingAgent
from api.law_agent.service import LawAgent

import langchain
langchain.debug = True

load_dotenv()
# async def define_law_agent(memory):
#     return await LawAgent.create(checkpointer=memory)

@asynccontextmanager
async def lifespan(app: FastAPI):
    memory = MemorySaver()
    app.law_agent = await LawAgent.create(checkpointer=memory)
    app.base_agent = BaseAgent(checkpointer=memory)
    app.applyhome_agent = ApplyhomeAgent(checkpointer=memory)
    app.pdf_agent = PDFAgent(checkpointer=memory)
    app.routing_agent = RoutingAgent(checkpointer=memory)
    yield
    
app = FastAPI(lifespan=lifespan)
# memory = MemorySaver()
# app.base_agent = BaseAgent(checkpointer=memory)
# app.applyhome_agent = ApplyhomeAgent(checkpointer=memory)
# app.pdf_agent = PDFAgent(checkpointer=memory)
# app.law_agent = define_law_agent(memory=memory)
# app.routing_agent = RoutingAgent()


from api.base_agent.router import router as base_agent_router
from api.applyhome_agent.router import router as applyhome_agent_router
from api.pdf_agent.router import router as pdf_agent_router
from api.routing_agent.router import router as routing_agent_router
from api.law_agent.router import router as law_agent_router

app.include_router(base_agent_router)
app.include_router(applyhome_agent_router)
app.include_router(pdf_agent_router)
app.include_router(law_agent_router)
app.include_router(routing_agent_router)

@app.get("/")
def hello():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
