from langchain_mcp_adapters.client import MultiServerMCPClient, load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

from typing import Optional, Literal
from langchain_core.tools import Tool

import asyncio

from ..base_agent.service import BaseAgent
from langgraph.types import Checkpointer
from langgraph.store.base import BaseStore

from .schema import LawAgentState
import os
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain_openai.chat_models import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama

"""
        __START__
            |
          AGENT
            |
            |
     --------------------
    |                   |
LAWTool            __END__
"""

class LawAgent(BaseAgent):
    @classmethod
    async def create(
        cls,
        checkpointer: Optional[Checkpointer] = None,
        store: Optional[BaseStore] = None,
    ) -> 'LawAgent':
        """비동기 팩토리 메서드로 LawAgent 객체 생성 및 초기화"""
        instance = cls(checkpointer=checkpointer, store=store)
        await instance.initialize()
        return instance
    
    def __init__(
        self,
        checkpointer: Optional[Checkpointer] = None,
        store: Optional[BaseStore] = None,
    ):
        # MCP client 초기화
        self.mcp_client = MultiServerMCPClient({
            "law_tool": {
                "command": "python3",
                "args": ["/home/data/app/tools/mcp_server/server.py"],  # MCP server 진입점
                "transport": "stdio",
            }
        })
        self.checkpointer = checkpointer
        self.store = store
        
        # 동기적으로 초기화 가능한 부분 처리
        api_key = os.getenv("OPENAI_API_KEY", "ollama")
        model_name = os.getenv("OPENAI_API_MODEL", "gpt-4o-mini")
        if api_key == "ollama":
            self.model = ChatOllama(model=model_name, temperature=0, streaming=True)
        else:
            self.model = ChatOpenAI(model=model_name, temperature=0, streaming=True)
        

    async def initialize(self): 
        """도구 로드 후 workflow를 세팅"""
        try:
            self.tool_classes = await self.mcp_client.get_tools()
            self.tool_node = ToolNode(self.tool_classes)
            self.model = self.model.bind_tools(self.tool_classes)
            self.workflow = self.init_workflow()
            self.workflow = self.workflow.compile(
                checkpointer=self.checkpointer,
                store=self.store,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LawAgent: {str(e)}")

        
    # def init_tools(self):
    #     tools = [
    #         Tool(
    #             name="pdf_url",
    #             func=self._mcp_tool_caller("pdf_url"),
    #             description="법령 PDF URL을 검색. Input: {'query': 법령 키워드, 예: '자동차'}"
    #         ),
    #         Tool(
    #             name="load_pdf",
    #             func=self._mcp_tool_caller("load_pdf"),
    #             description="법령 PDF 내용을 로드"
    #         ),
    #         Tool(
    #             name="download_pdf",
    #             func=self._mcp_tool_caller("download_pdf"),
    #             description="법령 PDF 파일을 다운로드. Input: {'pdf_urls': url을 담고 있는 리스트, 'output_dir':저장시킬 위치}"
    #         ),
    #         Tool(
    #             name="retrieve",
    #             func=self._mcp_tool_caller("retrieve"),
    #             description="법령 PDF에서 질문에 관련된 내용을 검색. Input: {'question': 궁금한 질의, 'pdf_paths':파일 위치}"
    #         ),
    #     ]
    #     return tools
    
    # def _mcp_tool_caller(self, tool_name):
    #     """MCP client tool 호출 래퍼"""
    #     async def _call(input):
    #         try:
    #             result = await self.mcp_client.call("law_tool", {
    #                 "method": tool_name,
    #                 "params": input
    #             })
    #             return result
    #         except Exception as e:
    #             return f"Error calling MCP tool '{tool_name}': {str(e)}"
    #     return _call
    
if __name__ == "__main__":
    from langgraph.checkpoint.memory import MemorySaver
    from langchain_core.messages import HumanMessage
    from dotenv import load_dotenv
    load_dotenv()

    agent = LawAgent(checkpointer=MemorySaver())

    state = LawAgentState(
        messages=[
            HumanMessage(content="자동차 법률 pdf 찾아줘.")
            # HumanMessage(content="잠실역 공고문의 계약기간을 알려줘.")
        ],
        # is_last_step=False,
        # remaining_steps=5,
    )
    config = {
        "configurable": {
            "thread_id": "thread-1",
            "user_id": "user-1",
        }
    }

    async def call_astream():
        async for chunk in agent.workflow.astream(state, config, stream_mode='values'):
            for state_node, state_value in chunk.items():
                if state_node == "messages":
                    state_value[-1].pretty_print()
    import asyncio
    asyncio.run(call_astream())