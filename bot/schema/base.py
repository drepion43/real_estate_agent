from typing import TypedDict


class BaseResponse(TypedDict):
    content: str
    tags: list[str]
    event: dict[str, str]
    config: dict[str, str]
