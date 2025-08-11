from langchain_core.messages import HumanMessage, AIMessage

from api.base_agent.schema import BaseAgentState


def parse_messages(state: BaseAgentState) -> list[HumanMessage | AIMessage]:
    return [
        HumanMessage(content=m.content)
        if m.type == "human"
        else AIMessage(content=m.content)
        for m in state["messages"]
    ]
