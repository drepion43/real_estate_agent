import os
import json

from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun

from typing import Optional, Type, List

from .crawler_tool1 import *
from .crawler_tool2 import *
from .cralwer_tool3_selenium import *

class CrawlInfoInput(BaseModel):
    types: str = Field(
        description="특정 지역의 특정 정보를 추출합니다. 선택할 수 없을시 쳥년안심주택을 선택합니다.",
        example=["청년안심주택", "천호한강청년주택", "서울대청년주택", "서울대센터스퀘어", "최강타워"]
    )

class CrawlInfoTool(BaseTool):
    name: str = "CrawlInfoTool"
    description: str = (
        "특정 지역의 주택 관련 정보를 수집하는 도구입니다."
        "사용자가 입력한 지역을 기준으로 다양한 주택 정보를 제공합니다."
        "예: 사용자가 '청년안심주택'을 요청하면 해당 지역의 관련 공고를 검색하여 반환합니다."
    )
    args_schema: Type[BaseModel] = CrawlInfoInput

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(
        self,
        types: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        
        json_path = os.path.join(os.path.dirname(__file__), 'house_types.json')
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        data_list = globals()[f"{data[types]}"]()

        return data_list
    
    async def _arun(
        self,
        types: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        json_path = os.path.join(os.path.dirname(__file__), 'house_types.json')
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        data_list = globals()[f"{data[types]}"]()

        return data_list
    
if __name__ == "__main__":
    tool = CrawlInfoTool()
    result = tool.invoke({
        "types": "관악구"
    })
    print(result)