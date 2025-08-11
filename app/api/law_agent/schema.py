from pydantic import BaseModel

from ..base_agent.schema import BaseAgentState, BaseAgentConfig


class LawAgentState(BaseAgentState):
    pass


class LawAgentConfig(BaseAgentConfig):
    pass


class LawAgentRouterScheme(BaseModel):
    state: LawAgentState
    config: LawAgentConfig