from typing import Optional

from .base import BaseResponse


class ApplyhomeResponse(BaseResponse):
    tool_inputs: Optional[dict[str, str]]
