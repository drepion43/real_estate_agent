from typing import Optional

from .base import BaseResponse


class LawResponse(BaseResponse):
    tool_inputs: Optional[dict[str, str]]
