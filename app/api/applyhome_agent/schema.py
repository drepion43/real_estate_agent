from pydantic import BaseModel

from ..base_agent.schema import BaseAgentState, BaseAgentConfig


class ApplyhomeAgentState(BaseAgentState):
    pass


class ApplyhomeAgentConfig(BaseAgentConfig):
    pass


class ApplyhomeAgentRouterScheme(BaseModel):
    state: ApplyhomeAgentState
    config: ApplyhomeAgentConfig
