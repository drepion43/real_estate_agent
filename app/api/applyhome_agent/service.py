from .schema import ApplyhomeAgentState
from tools import CrawlApplyHomeTool, PDFMultiVectorRetrievalTool, CrawlInfoTool
from ..base_agent.service import BaseAgent


"""
        __START__
            |
          AGENT
            |
            |
     --------------------
    |                   |
CrawlTool            __END__

"""


class ApplyhomeAgent(BaseAgent):

    def init_tools(self):
        tools = [
            CrawlApplyHomeTool(), 
            CrawlInfoTool(),
            PDFMultiVectorRetrievalTool
        ]
        
        return tools

if __name__ == "__main__":
    from langgraph.checkpoint.memory import MemorySaver
    from langchain_core.messages import HumanMessage
    from dotenv import load_dotenv
    load_dotenv()

    agent = ApplyhomeAgent(checkpointer=MemorySaver())

    state = ApplyhomeAgentState(
        messages=[
            HumanMessage(content="서울 오피스텔 공고 찾아줘.")
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