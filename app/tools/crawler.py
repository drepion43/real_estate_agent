import time
from typing import Optional, Type, TypedDict, Literal
from pydantic import BaseModel, Field

import os
import requests

from bs4 import BeautifulSoup
import markdownify

from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)


import json
from urllib.request import Request, urlopen
from urllib import parse
import datetime

class CrawlApplyHomeToolInput(BaseModel):
    user_query: str = Field(
        description="사용자의 검색어 전체입니다. 사용자의 검색은 대한민국의 아파트의 청약 등 주택과 관련한 내용을 포함합니다.",
    )
    house_type: str = Field(
        description="아파트, 민간사전청약아파트, 민간임대오피스텔, 공공지원민간임대 중 선택합니다. 특정 유형을 선택할 수 없다면 '전체'를 선택하세요.",
        example=["전체", "아파트", "민간사전청약아파트", "민간임대오피스텔", "공공지원민간임대"],
    )
    jiyeok: str = Field(
        description="지역 이름을 추출합니다. 특정 지역을 추출할 수 없다면 '전체'를 선택하세요",
        examples=["전체", "서울특별시", "대구광역시", "전라남도", "부산광역시"]
    )

class CrawlApplyHomeTool(BaseTool):

    name: str = "CrawlTool"
    description: str = "대한민국의 아파트의 청약, 민간사전청약아파트, 민간임대오피스텔 등의 정보를 수집할 수 있는 tool입니다."
    args_schema: Type[BaseModel] = CrawlApplyHomeToolInput
    
    data_url: str = "https://www.applyhome.co.kr/ai/aib/selectSubscrptCalender.do"
    
    info_url: list = [
        "https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancDetail.do", # se : 01 or 09
        "https://www.applyhome.co.kr/ai/aia/selectAPTRemndrLttotPblancDetailView.do", # se : 04 or 06 or 11
        "https://www.applyhome.co.kr/ai/aia/selectPRMOLttotPblancDetailView.do"
    ]
    
    data_headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    
    # mbHouseDetailSeClass: dict[str, str] = {
    #     "lb_special": 'APT 특별공급',
    #     "lb_one": 'APT 1순위',
    #     "lb_two": 'APT 2순위',
    #     "lb_simin": '공공지원민간임대',
    #     "lb_office": '오피스텔/생활숙박시설/도시형생활주택/민간임대',
    #     "lb_resid": '무순위',
    #     "lb_apo": '임의공급',
    #     "lb_resid2": '취소후재공급',
    #     "lb_adv_special": '민간사전청약 APT 특별공급',
    #     "lb_adv_one": '민간사전청약 APT 1순위',
    #     "lb_adv_two": '민간사전청약 APT 2순위',
    # }
        
    # houseSeClass: dict[str, str] = {
    #     '01' : 'lb_special',
    #     '02' : 'lb_one',
    #     '03' : 'lb_two',
    #     '04' : 'lb_simin',
    #     '05' : 'lb_office',
    #     '06' : 'lb_resid',
    #     '07' : 'lb_resid2',
    #     '08' : 'lb_adv_special',
    #     '09' : 'lb_adv_one',
    #     '10' : 'lb_adv_two',
    #     '11' : 'lb_apo'
    # }
    type_keys: dict[str, list] = {
        "아파트": ["01","02", "03", "06", "07", "11"],
        "민간사전청약아파트": ["08", "09", "10"],
        "민간임대오피스텔": ["05"],
        "공공지원민간임대": ["04"],
    }

    jiyeok_keys: dict[str, list] = {
        "서울특별시": ["서울"],
        "광주광역시": ["광주"],
        "대구광역시": ["대구"],
        "대전광역시": ["대전"],
        "부산광역시": ["부산"],
        "세종특별자치시": ["세종"],
        "울산광역시": ["울산"],
        "인천광역시": ["인천"],

        "강원특별자치도": ["강원"],
        "경기도": ["경기"],
        "경상남도": ["경남"],
        "경상북도": ["경북"],
        "전라남도": ["전남"],
        "전라북도": ["전북"],
        "제주특별자치도": ["제주"],
        "충청남도": ["충남"],
        "충청북도": ["충북"],
    }
    
    enum_jiyeok : str = "서울 광주 대구 대전 부산 세종 울산 인천 강원 경기 경북 \
        경남 전남 전북 제주 충남 충북"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def _start(self):
        today_yyyymm = datetime.datetime.today().strftime("%Y%m") 
        data_params = {
            "reqData": {
                "inqirePd": today_yyyymm
                }
        }
        
        response = requests.post(self.data_url, json=data_params, headers=self.data_headers)
        response.raise_for_status()
        response_data = response.json()
        data_list = response_data["schdulList"]
        return data_list
    
    def _date_filtering(self, data_list):
        today_yyyymmdd = datetime.datetime.today().strftime("%Y%m%d") 
        result = dict()
        return 
            
        
    def _address_api(self,
                     keyword,
                     **kwargs):
        urls = 'http://www.juso.go.kr/addrlink/addrLinkApi.do'
        confmKey = os.getenv('JUSO_API_KEY') # 필수 값 승인키
        
        params = {
            'keyword': keyword,
            'confmKey': confmKey,
            'resultType': 'json'
        }
        
        if kwargs: # 필수 값이 아닌 변수를 params에 추가
            for key, value in kwargs.items():
                params[key] = value
        params_str = parse.urlencode(params) # dict를 파라미터에 맞는 포맷으로 변경
        
        url = '{}?{}'.format(urls, params_str)
        response = urlopen(url) # Request 객체로 urlopen을 호출하면 요청된 URL에 대한 응답 객체를 반환
        result_xml = response.read().decode('utf-8') # response를 읽고 utf-8로 변형
        result = json.loads(result_xml)
        status = result['results']['common']['errorMessage']
        roadAddr_list = []
        lengths = len(result['results']['juso'])
        if status == '정상':
            for idx in range(lengths):
                roadAddr_list.append(result['results']['juso'][idx]['siNm'])
        roadAddr_list = set(roadAddr_list)
        return roadAddr_list
    
    def _transform_address(self,
                           jiyeok: str) -> list:
        add_lists = self._address_api(jiyeok)

        result = set()
        for add_list in add_lists:
            result.add(add_list)
        return list(result)

    def _run(
        self,
        user_query: str,
        house_type: str,
        jiyeok: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:

        data_list = self._start()
        
        house_type_list = []
        jiyeok_list = []
        
        if jiyeok in self.enum_jiyeok:
            jiyeok_list = [jiyeok]
        else:
            jiyeok = self._transform_address(jiyeok=jiyeok)        
        

        
        if house_type != "전체":
            h_type_key = self.type_keys[house_type]
            house_type_list.extend(h_type_key)
        if jiyeok != "전체" and not jiyeok_list:
            for sido in jiyeok: 
                jiyeok_key = self.jiyeok_keys[sido]
                jiyeok_list.extend(jiyeok_key)

        data_list = self._filtering(house_type=house_type_list,
                                    jiyeok=jiyeok_list,
                                    data_list=data_list)
        # 상위 8개만
        data_list = data_list[:8]

        posts = [self._post_handler(data) for data in data_list]

        return posts

    async def _arun(
        self,
        user_query: str,
        house_type: str,
        jiyeok: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:

        data_list = self._start()
        
        house_type_list = []
        jiyeok_list = []
        
        if jiyeok in self.enum_jiyeok:
            jiyeok_list = [jiyeok]
        else:
            jiyeok = self._transform_address(jiyeok=jiyeok)
        
        
        if house_type != "전체":
            h_type_key = self.type_keys[house_type]
            house_type_list.extend(h_type_key)
        if jiyeok != "전체" and not jiyeok_list:
            for sido in jiyeok: 
                jiyeok_key = self.jiyeok_keys[sido]
                jiyeok_list.extend(jiyeok_key)
        
        data_list = self._filtering(house_type=house_type_list,
                                    jiyeok=jiyeok_list,
                                    data_list=data_list)
        # 상위 8개만
        data_list = data_list[:8]
        
        posts = [self._post_handler(data) for data in data_list]        
        
        return posts
    
    def _filtering(
        self,
        house_type: list,
        jiyeok: str,
        data_list: list
    ) -> list:
        new_data_list = []
        for data in data_list:
            # 집 필터 / 지역 필터
            if house_type and jiyeok:
                if data['SUBSCRPT_AREA_CODE_NM'] in jiyeok and data['HOUSE_SECD'] in house_type:
                    new_data_list.append(data)
            # 집은 필터 / 지역은 전체
            elif house_type and not jiyeok:
                if data['HOUSE_SECD'] in house_type:
                    new_data_list.append(data)
            # 집은 전체 / 지역은 필터
            elif not house_type and jiyeok:
                if data['SUBSCRPT_AREA_CODE_NM'] in jiyeok:
                    new_data_list.append(data)
            # 집과 지역 전체
            else:
                new_data_list.append(data)

        return new_data_list
            
    
    def _download_file(self, url, file_name):
        response = requests.get(url)
        if response.status_code == 200:
            file_name = "./" + file_name
            with open(file_name, 'wb') as file:
                file.write(response.content)
                
    def _parsing_data(self, data):
        result = {
            "title": data["HOUSE_NM"],
            "jiyeok": data["SUBSCRPT_AREA_CODE_NM"],
            "date": data["IN_DATE"],
            "house_manage_code": data["HOUSE_MANAGE_NO"],
            "house_pblanc_code": data["PBLANC_NO"],
            "house_secd": data["HOUSE_SECD"]
        }
        
        return result

    def _post_handler(self, data):
        extract_data = self._parsing_data(data)
        # 파일 이름
        file_name = f'{extract_data["title"]}_{extract_data["jiyeok"]}_{extract_data["date"]}.pdf'
        
        # 세부내용 url로 데이터 post
        detail_params = {
            "houseManageNo": extract_data["house_manage_code"],
            "pblancNo": extract_data["house_pblanc_code"],
            "houseSecd": extract_data["house_secd"],
            "gvPgmId": "AIB01M01"
        }
        detail_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }
        
        if extract_data["house_secd"] == "01" or extract_data["house_secd"] == "09":
            detail_url = self.info_url[0]
        elif extract_data["house_secd"] == "04" or extract_data["house_secd"] == "06" or extract_data["house_secd"] == "11":
            detail_url = self.info_url[1]
        else:
            detail_url = self.info_url[2]
        
        detail_response = requests.post(detail_url, data=detail_params, headers=detail_headers, verify=False)
        md_content = markdownify.markdownify(detail_response.text)

        detail_response.raise_for_status()
        soup = BeautifulSoup(detail_response.content, 'html.parser')
        link_tag = soup.find("a", class_="radius_btn")
        down_link = link_tag.get("href")
        self._download_file(down_link, file_name)
        
        ret = {
            "data_hmno": extract_data,
            "md_content": md_content, "pdf_url": down_link
        }
        return ret
    
if __name__ == "__main__":
    tool = CrawlApplyHomeTool()
    tool.invoke({
        "user_query": "",
        "house_type": "전체",
        "jiyeok": "대전",
        # "jiyeok": "전체",
    })
