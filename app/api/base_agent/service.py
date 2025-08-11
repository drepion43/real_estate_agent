import os
from typing import Optional, Literal

from langchain_core.tools import Tool
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai.chat_models import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama

from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Checkpointer
from langgraph.store.base import BaseStore
from langgraph.utils.runnable import RunnableCallable

from tools.example_tools import get_current_time, multiply
from .schema import BaseAgentState


class BaseAgent:

    def __init__(
        self,
        checkpointer: Optional[Checkpointer] = None,
        store: Optional[BaseStore] = None,
    ):
        self.tool_classes = self.init_tools()
        self.tool_node = ToolNode(self.tool_classes)

        api_key = os.getenv("OPENAI_API_KEY", "ollama")
        model_name = os.getenv("OPENAI_API_MODEL", "gpt-4o-mini")
        if api_key == "ollama":
            self.model = ChatOllama(model=model_name, temperature=0, streaming=True)
        else:
            self.model = ChatOpenAI(model=model_name, temperature=0, streaming=True)

        self.model = self.model.bind_tools(self.tool_classes)

        self.workflow = self.init_workflow()
        self.workflow = self.workflow.compile(
            checkpointer=checkpointer,
            store=store,
        )

    def init_tools(self):
        tools = [
            Tool(
                name="getCurrentTime",  # Name of the tool
                func=get_current_time,  # Function that the tool will execute
                description="Useful for when you need to know the current time",
            ),
            Tool(
                name="multiply",
                func=multiply,
                description="Useful for when you need to multiply two numbers together",
            )
        ]
        return tools

    def init_workflow(self):
        workflow = StateGraph(BaseAgentState)
        # Define the two nodes we will cycle between
        workflow.add_node("agent", RunnableCallable(self.call_model, self.acall_model))
        workflow.add_node("tools", self.tool_node)

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        workflow.set_entry_point("agent")

        workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`,
            # This means these are the edges taken after the `agent node is called.
            "agent",
            # Next, we pass in the function that will determine which node is called next.
            self._should_continue,
        )

        workflow.add_edge("tools", "agent")
        return workflow

    def _should_continue(self, state: BaseAgentState) -> Literal["tools", "__end__"]:
        messages = state["messages"]
        last_message = messages[-1]

        if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
            return "__end__"
        else:
            return "tools"

    def call_model(
        self,
        state: BaseAgentState,
        config: RunnableConfig
    ) -> BaseAgentState:
        state_runnable = RunnableCallable(lambda s: s["messages"], name="StateModifier")
        model_runnable = state_runnable | self.model
        response = model_runnable.invoke(state, config)
        has_tool_calls = isinstance(response, AIMessage) and response.tool_calls
        
        # 5회 제한 로직 추가
        if (
            "remaining_steps" in state
            and state["remaining_steps"] <= 0
            and has_tool_calls
        ):
            return {
                "messages": [
                    AIMessage(
                        id=response.id,
                        content="Error: The agent was unable to complete the task after multiple attempts."
                    )
                ]
            }

        if (
            (
                "remaining_steps" not in state
                and state["is_last_step"]
                and has_tool_calls
            )
            or (
                "remaining_steps" in state
                and state["remaining_steps"] < 2
                and has_tool_calls
            )
        ):
            return {
                "messages": [
                    AIMessage(
                        id=response.id,
                        content="Sorry, need more steps to process this request.",
                    )
                ]
            }

        return {"messages": [response]}

    async def acall_model(
        self,
        state: BaseAgentState,
        config: RunnableConfig
    ) -> BaseAgentState:
        state_runnable = RunnableCallable(lambda s: s["messages"], name="StateModifier")
        model_runnable = state_runnable | self.model
        response = await model_runnable.ainvoke(state, config)
        has_tool_calls = isinstance(response, AIMessage) and response.tool_calls
        
        # 5회 제한 로직 추가
        if (
            "remaining_steps" in state
            and state["remaining_steps"] <= 0
            and has_tool_calls
        ):
            return {
                "messages": [
                    AIMessage(
                        id=response.id,
                        content="Error: The agent was unable to complete the task after multiple attempts."
                    )
                ]
            }

        if (
            (
                "remaining_steps" not in state
                and state["is_last_step"]
                and has_tool_calls
            )
            or (
                "remaining_steps" in state
                and state["remaining_steps"] < 2
                and has_tool_calls
            )
        ):
            return {
                "messages": [
                    AIMessage(
                        id=response.id,
                        content="Sorry, need more steps to process this request.",
                    )
                ]
            }

        return {"messages": [response]}
