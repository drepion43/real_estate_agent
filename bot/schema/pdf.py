from typing import Optional

from .base import BaseResponse


class PDFResponse(BaseResponse):
    # pdf_path: list[str]
    tool_inputs: Optional[dict[str, str]]
