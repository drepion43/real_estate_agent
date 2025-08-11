# from typing import TypedDict, Sequence, Annotated             # python 3.12 이상에서만 돌아감
from typing_extensions import TypedDict, Sequence, Annotated    # python 3.10 버젼
from pydantic import BaseModel

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.managed import IsLastStep, RemainingSteps


# langgraph/prebuilt/chat_agent_executor.py: AgentState
class BaseAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    is_last_step: IsLastStep
    remaining_steps: RemainingSteps


class BaseConfig(TypedDict):
    thread_id: str
    user_id: int


class BaseAgentConfig(TypedDict):
    configurable: BaseConfig


class BaseAgentRouterScheme(BaseModel):
    state: BaseAgentState
    config: BaseAgentConfig
