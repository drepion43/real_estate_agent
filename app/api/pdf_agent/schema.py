from typing import Annotated, List, Optional
from pydantic import BaseModel, Field

from ..base_agent.schema import BaseAgentState, BaseAgentConfig


class PDFAgentState(BaseAgentState):

    # documents: Annotated[List[str], "List of documents"]
    # rewrite_cnt: Annotated[int, "Count rewrite called"]
    pass

class PDFAgentConfig(BaseAgentConfig):
    # pdf_path: list[str]
    pass


class PDFAgentRouterScheme(BaseModel):
    state: PDFAgentState
    config: PDFAgentConfig


# class GradeDocumentsScheme(BaseModel):

#     binary_score: list[str] = Field("Documents are relevant to the question, 'yes' or 'no'.")
