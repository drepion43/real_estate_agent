# import chromedriver_autoinstaller
import time
import sys
import os

# 현재 파일의 상위 디렉토리 경로를 찾기
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 상위 디렉토리에 있는 target_folder를 sys.path에 추가
sys.path.append(parent_dir)

import requests
import urllib3

from bs4 import BeautifulSoup
from urllib.parse import unquote
from tools.cralwer_tool3_selenium import *
from core.pathinfo import *
from urllib.parse import unquote
from dotenv import load_dotenv
load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

############################### 청년안심주택 공식 사이트 ###############################
## cohomeList -> ajax
def fetch_board_official() -> list:
    board_data = []
    
    api_url = OFFICIAL_URL_API

    # 최대 10개 페이지
    for p in range(1, 2):
        params = {
            "bbsId": "BMSR00015",
            "pageIndex": p,
            "searchAdresGu": "",
            "searchCondition": "",
            "searchKeyword": ""
        }
        response = requests.post(api_url, data=params)
        response.raise_for_status()
        data = response.json()
        
        length = len(data['resultList'])
        for i in range(length):
            apply_type = "공공" if data['resultList'][i]['optn2'] == '1' else "민간"
            title = data['resultList'][i]['nttSj']
            content = data['resultList'][i]['content']
            date = data['resultList'][i]['optn1']
            department = data['resultList'][i]['optn3']
            apply_date = data['resultList'][i]['optn4']
            soup = BeautifulSoup(content, 'html.parser')
            links = [a["href"] for a in soup.find_all("a")]
            board_data.append((title, date, links))

    return board_data

# =============================================================================================================

############################### 강남구 사이트 ###############################
def fetch_gangnamgu_list() -> list: # PHP 형태, Header필요, Data 필요 X
    
    url = GANGNAMGU_LIST_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "http://www.listgangnam.co.kr/",
            "Content-Type": "text/html; charset=utf-8"
        }
        
        response = requests.get(url, headers=headers, verify=False)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select('tbody tr')
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('div.bo_tit a').get_text(strip=True)
            date = data_list[index].select_one('td.td_datetime').get_text(strip=True)
            
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangnamgu_theone() -> list: # PHP 형태, Header필요, Data 필요 X
    
    url = GANGNAMGU_THEONE_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "https://www.theoneys.co.kr/",
            "Content-Type": "text/html; charset=utf-8"
        }
        
        response = requests.get(url, headers=headers, verify=False)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select('div.li_board ul.li_body')
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('li.tit a.list_text_title span').get_text(strip=True)
            date = data_list[index].select_one('li.time').get_text(strip=True)
            
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangnamgu_elga() -> list: # PHP 형태, Header필요, Data 필요 X
    
    url = GANGNAMGU_ELGA_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Content-Type": "text/html; charset=EUC-KR"
        }
        
        params = {           
            "id": "notice"
            }
        
        response = requests.get(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select('tbody#div_article_contents tr[height="36"]')
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('td[align="left"] font a').get_text(strip=True)
            date = data_list[index].select('td')[-1].get_text(strip=True)
            
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangnamgu_maestro() -> list: # PHP 형태, Header필요, Data 필요 X
    
    url = GANGNAMGU_MAESTRO_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "https://maestrosamseong.com/",
            "Content-Type": "text/html; charset=utf-8"
        }
        
        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('td.td_left a').get_text(strip=True)
            date = data_list[index].select_one('td.mobile_x').get_text(strip=True)
            
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangnamgu_dgsummit() -> list: # PHP 형태, Header필요, Data 필요 X
    
    url = GANGNAMGU_DGSUMMIT_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "https://www.dg-summit.co.kr/49",
            "Content-Type": "text/html; charset=utf-8"
        }
        
        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.li_board ul.li_body")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('a.list_text_title span').get_text(strip=True)
            date = data_list[index].select_one('li.time')
            date = date.get_text(strip=True) if date else "날짜없음"
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data

# =============================================================================================================

############################### 강동구 사이트 ###############################
def fetch_gangdongu_cheonho() -> list:
    # 최근 5개의 페이지에 대한 공고만 가져오기
    board_data = []
    for p in range(1, 2):
        url = f'{GANGDONGU_CHEONHO_URL}&page={p}'
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.select("#bo_list tbody tr")
            for idx, row in enumerate(rows):
                title_element = row.select_one("td.td_subject a")
                title = title_element.text.strip() if title_element else "No title"
                link = title_element.get('href')
                link = url + link[1:]
                date_element = row.select_one("td.td_num")
                date = date_element.text.strip() if date_element else "No date"
                board_data.append((title, link))

    return board_data
def fetch_gangdongu_hyosung() -> list: # PHP 형태, Header필요, Data 필요 X
    
    url = GANGDONGU_HYOSUNG_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "http://www.cheonho2030.com/",
            "Content-Type": "text/html; charset=UTF-8"
        }
                
        response = requests.get(url)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.news-list li")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('div.tit a').get_text(strip=True)
            date = data_list[index].select_one('div.date')
            date = date.get_text(strip=True) if date else "날짜없음"
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangdongu_gildong() -> list: # PHP 형태, Header필요, Data 필요 X
    
    url = GANGONDGU_GILDONG_API_URL

    try:        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "https://www.gildonglife.co.kr/",
            "Content-Type": "text/html; charset=utf-8"
            }

        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.li_board ul.li_body")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('a.list_text_title span').get_text(strip=True)
            date = data_list[index].select_one('li.time').get_text(strip=True)
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data

# =============================================================================================================

############################### 강북구 사이트 ###############################
# 없음
# =============================================================================================================

############################### 강서구 사이트 ###############################
def fetch_gangseogu_centersquarebs() -> list:  # HTML 형태, Header 필요 X,
        
    url = GANGSEOGU_CENTERSQUAREBS_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("ul.li_body.notice_body.holder")
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one(" li.tit.show_right_tools a.list_text_title._fade_link").get_text(strip=True)
            date = data_list[index].select_one("li.time").get_text(strip=True)

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangseogu_centersquare() -> list:  # JSON 형태, Header, Data 필요,
        
    url = GANGSEOGU_CENTERSQUARE_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://centersquare.modoo.at/?link=bpjvg4uq",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://centersquare.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {           
            "cid": "bpjvg4uq",
            "startNo": 1,
            "count": 8,
            "searchMode": 0,
            "replyAttr": 1
            }

        # GET 요청 보내기
        response = requests.post(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")

        # JSON 응답 데이터 파싱
        data = response.json()
        board_data = []

        # 게시물 리스트 추출
        for index, post in enumerate(data.get("messageList", [])):
            title = post.get("subject", "제목 없음")
            date = post.get("regTmStr", "날짜 없음")
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangseogu_bonum() -> list: # JSON 형태, Header, Data 필요
    
    url = GANGSEOGU_BONUM_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://bonumhaus2030.modoo.at/?link=czpnlnoj&page=1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://bonumhaus2030.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {           
            "cid": "czpnlnoj",
            "startNo": 1,
            "count": 8,
            "searchMode": 0,
            "replyAttr": 1
            }

        # GET 요청 보내기
        response = requests.post(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")

        # JSON 응답 데이터 파싱
        data = response.json()
        board_data = []

        # 게시물 리스트 추출
        for index, post in enumerate(data.get("messageList", [])):
            title = post.get("subject", "제목 없음")
            date = post.get("regTmStr", "날짜 없음")
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangseogu_fortuna() -> list: # JSON 형태, Header, Data 필요
    
    url = GANGSEOGU_FORTUNA_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://fortunablue.modoo.at/?link=dcn8otgl",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://fortunablue.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {           
            "cid": "dcn8otgl",
            "startNo": 1,
            "count": 8,
            "searchMode": 0,
            "replyAttr": 1
            }

        # GET 요청 보내기
        response = requests.post(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")

        # JSON 응답 데이터 파싱
        data = response.json()
        board_data = []

        # 게시물 리스트 추출
        for index, post in enumerate(data.get("messageList", [])):
            title = post.get("subject", "제목 없음")
            date = post.get("regTmStr", "날짜 없음")
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangseogu_im2030() -> list: # JSON 형태, Header, Data 필요
    
    url = GANGSEOGU_IM2030_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://im2030.modoo.at/?link=dv1398ka",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://im2030.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {           
            "cid": "dv1398ka",
            "startNo": 1,
            "count": 8,
            "searchMode": 0,
            "replyAttr": 1
            }

        # GET 요청 보내기
        response = requests.post(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")

        # JSON 응답 데이터 파싱
        data = response.json()
        board_data = []

        # 게시물 리스트 추출
        for index, post in enumerate(data.get("messageList", [])):
            title = post.get("subject", "제목 없음")
            date = post.get("regTmStr", "날짜 없음")
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangseogu_fltower() -> list: # JSON 형태, Header, Data 필요
    
    url = GANGSEOGU_FLTOWER_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://fltower.modoo.at/?link=soo8sobp",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://fltower.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {           
            "cid": "soo8sobp",
            "startNo": 1,
            "count": 8,
            "searchMode": 0,
            "replyAttr": 1
            }

        # GET 요청 보내기
        response = requests.post(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")

        # JSON 응답 데이터 파싱
        data = response.json()
        board_data = []

        # 게시물 리스트 추출
        for index, post in enumerate(data.get("messageList", [])):
            title = post.get("subject", "제목 없음")
            date = post.get("regTmStr", "날짜 없음")
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangseogu_lcrew() -> list: # JSON 형태, Header, Data 필요
    
    url = GANGSEOGU_LCREW_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://youngtower.modoo.at/?link=94gu5os0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://youngtower.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {           
            "cid": "94gu5os0",
            "startNo": 1,
            "count": 8,
            "searchMode": 0,
            "replyAttr": 1
            }

        # GET 요청 보내기
        response = requests.post(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")

        # JSON 응답 데이터 파싱
        data = response.json()
        board_data = []

        # 게시물 리스트 추출
        for index, post in enumerate(data.get("messageList", [])):
            title = post.get("subject", "제목 없음")
            date = post.get("regTmStr", "날짜 없음")
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_gangseogu_ujs() -> list:  # HTML 형태, Header 필요 X,
        
    url = GANGSEOGU_UJS_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        response = requests.get(url, headers=headers, verify=False)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div#notice ul li")
        board_data = []
        for index in range(1, len(data_list)):
            title = data_list[index].select_one("a").get_text(strip=True)
            date = data_list[index].select_one("span").get_text(strip=True)

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data

# =============================================================================================================

############################### 관악구 사이트 ###############################
def fetch_gwanakgu_bx201() -> list:
    board_data = []
    
    api_url = GWANAKGU_BX201_URL_API
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://bx201seoul.modoo.at",  # 필요시 정확한 referer URL로 수정하세요.
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    cnt = 8
    
    # 요청에 필요한 매개변수 설정
    for p in range(1):
        params = {
            "cid": "3gs5oxwu",
            "startNo": 1 + p*cnt,
            "count": cnt,
            "searchMode": 0,
            "replyAttr": 1
        }
        session = requests.Session()

        response = session.post(api_url, data=params, headers=headers, verify=False)

        response.raise_for_status()

        response_data = response.json()
        length = len(response_data['messageList'])
        for i in range(length):
            img_list = []
            title = response_data['messageList'][i]['subject']
            # writer = response_data['messageList'][0]['loginId']
            date = response_data['messageList'][i]['regTmStr']
            img1 = response_data['messageList'][i]['image1']
            img2 = response_data['messageList'][i]['image2']
            img3 = response_data['messageList'][i]['image3']
            img4 = response_data['messageList'][i]['image4']
            img5 = response_data['messageList'][i]['image5']
            img_list.extend((img1, img2, img3, img4, img5))
            img_list = [img for img in img_list if len(img) > 0]
            
            board_data.append((title, img_list))
    
    return board_data
def fetch_gwanakgu_square() -> list:
    # header 얻기
    url = GWANAKGU_SQUARE_URL
    params = {
        "boardid": "notice",
        "sk": "",
        "sw": "",
        "category": "",
        "offset": 0
    }
    header_response = requests.get(url, data=params)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    total_size_content = soup.find('div', class_="total-page").get_text(strip=True)
    total_size = int(total_size_content.split(':')[-1])
    

    board_data = []
    
    # 페이지 돌아야 할 횟수
    page_cnt = total_size // 10
    for idx in range(1):
        page_params = {
            "boardid": "notice",
            "sk": "",
            "sw": "",
            "category": "",
            "offset": 0 + idx * 10
        }
        response = requests.get(url, data=page_params)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        rows = soup.select('.info')
        for index, row in enumerate(rows):
            title = row.select_one('.tit').get_text(strip=True)
            detail_link = row.select_one('.tit a').get('href')
            link = url + detail_link
            date = row.select_one('.date')
            board_data.append((title, link))
            
    return board_data
def fetch_gwanakgu_choigang() -> list:
    url = GWANAKGU_CHOIGANG_URL
    params = {
        "boardid": "notice",
        "sk": "",
        "sw": "",
        "category": "",
        "offset": 0
    }
    header_response = requests.get(url, data=params)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    total_size_content = soup.find('div', class_="total-page").get_text(strip=True)
    total_size = int(total_size_content.split(':')[-1])
    

    board_data = []
    
    # 페이지 돌아야 할 횟수
    page_cnt = total_size // 10
    for idx in range(1):
        page_params = {
            "boardid": "notice",
            "sk": "",
            "sw": "",
            "category": "",
            "offset": 0 + idx * 10
        }
        response = requests.get(url, data=page_params)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title_rows = soup.select('.tit')
        info_rows = soup.select('.info')
        for i in range(len(title_rows)):
            title = title_rows[i].select_one('a').get_text(strip=True)
            detail_link = title_rows[i].select_one('a').get('href')
            writer = info_rows[i].select_one('.name').get_text(strip=True)
            date = info_rows[i].select_one('.date').get_text(strip=True)
            link = url + detail_link
            board_data.append((title, link))
    return board_data    

# =============================================================================================================

############################### 광진구 사이트 ###############################
def fetch_gwangjingu_centum() -> list:
    url = GWANGJINGU_CENTUM_URL
    board_data = []

    for p in range(1, 2):
        params = {
            "bo_table": "news",
            "page": p,
        }

        header_response = requests.get(url, data=params)
        header_response.raise_for_status()
        soup = BeautifulSoup(header_response.content, 'html.parser')
        total_size_content = soup.select("#bo_list #bo_btn_top #bo_list_total")[0].get_text()
        # print(total_size)
        data_list = soup.select("#bo_list tbody td.td_subject")
        date_list = soup.select("#bo_list tbody td.td_datetime.lview")
        writer_list = soup.select("#bo_list tbody td.td_name.sv_use.lview")
        
        for i in range(len(data_list)):
            board_types = data_list[i].select_one('a.bo_cate_link').get_text(strip=True)
            detail_link = data_list[i].select_one('.bo_tit a').get('href')
            title = data_list[i].select_one('.bo_tit').get_text(strip=True)
            target = writer_list[i].get_text(strip=True)
            date = date_list[i].get_text(strip=True)
            board_data.append((title, detail_link))

    return board_data         
def fetch_gwangjingu_podium() -> list:
    api_url = GWANGJINGU_PODIUM_API_URL
    board_data = []
    total_count = 0
    params = {
        "isNotice": "true",
        # "searchKey": "all",
    }
    response_isno = requests.get(api_url, data=params)
    response_isno.raise_for_status()
    response_data = response_isno.json()
    total_count += int(response_data['summary']['totalCount'])
    data_list = response_data['notifications']

    for idx in range(total_count):
        title = data_list[idx]['subject']
        content = data_list[idx]['content']
        date = data_list[idx]['createdAt']
        _id = data_list[idx]['_id']
        link = GWANGJINGU_PODIUM_DETAIL_URL + _id
        board_data.append((title, link))
        
    return board_data
def fetch_gwangjingu_vival() -> list: # 셀레니움 사용
    driver = configure_driver(ignore_ssl=False, ignore_certfi=False)
    result = fetch_board_viva(driver=driver)
    return result
def fetch_gwangjingu_gunja() -> list:
    url = GWANGJINGU_GUNJA
    params = {
        "boardid": "notice",
        "sk": "",
        "sw": "",
        "category": "",
        "offset": 0
    }
    header_response = requests.get(url, data=params)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    total_size_content = soup.find('div', class_="total-page").get_text(strip=True)
    total_size = int(total_size_content.split(':')[-1])

    board_data = []
    
    # 페이지 돌아야 할 횟수
    page_cnt = total_size // 9
    for idx in range(1):
        page_params = {
            "boardid": "notice",
            "sk": "",
            "sw": "",
            "category": "",
            "offset": 0 + idx * 9
        }
        response = requests.get(url, data=page_params)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.select(".notice-list a")
        for row in rows:
            title = row.select_one('.tit').get_text(strip=True)
            date = row.select_one('.date').get_text(strip=True)[2:]
            link = row.get('href')
            link = GWANGJINGU_GUNJA + link
            board_data.append((title, link))
    return board_data
def fetch_gwangjingu_greentwoer() -> list:
    board_data = []
    keyword = "옥산그린타워"
    api_url = OFFICIAL_URL_API

    # 최대 10개 페이지
    for p in range(1, 2):
        params = {
            "bbsId": "BMSR00015",
            "pageIndex": p,
            "searchAdresGu": "",
            "searchCondition": "",
            "searchKeyword": ""
        }
        response = requests.post(api_url, data=params)
        response.raise_for_status()
        data = response.json()
        
        length = len(data['resultList'])
        for i in range(length):
            apply_type = "공공" if data['resultList'][i]['optn2'] == '1' else "민간"
            title = data['resultList'][i]['nttSj']
            content = data['resultList'][i]['content']
            date = data['resultList'][i]['optn1']
            department = data['resultList'][i]['optn3']
            apply_date = data['resultList'][i]['optn4']
            soup = BeautifulSoup(content, 'html.parser')
            links = [a["href"] for a in soup.find_all("a")]
            
            # 특정 키워드 포함 여부 확인 후 필터링
            if keyword in title:
                board_data.append((title, date, links))

    return board_data
# =============================================================================================================

############################### 구로구 사이트 ###############################
def fetch_gurogu_seizium() -> list:
        
    url = GUROGU_SEIZIUM_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://seizium-gb.com/center/notice?isNotice=false&searchKey=all&searchValue&page=1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
        
        params = {           
            "isNotice": "false",
            "searchKey": "all"
            }

        # GET 요청 보내기
        response = requests.get(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")

        # JSON 응답 데이터 파싱
        data = response.json()
        board_data = []

        # 게시물 리스트 추출
        for index, post in enumerate(data.get("notifications", [])):
            title = post.get("subject", "제목 없음")
            date = post.get("createdAt", "날짜 없음")
            date = date[0:10]
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data

# =============================================================================================================

############################### 금천구 사이트 ###############################


# =============================================================================================================

############################### 노원구 사이트 ###############################
def fetch_nowongu_initium() -> list:
    url = NOWONGU_INITIUM_URL
    params = {
        "boardid": "notice",
        "sk": "",
        "sw": "",
        "category": "",
        "offset": 0
    }
    header_response = requests.get(url, data=params)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    total_size_content = soup.find('div', class_="total-page").get_text(strip=True)
    total_size = int(total_size_content.split(':')[-1])
    board_data = []

    # 페이지 돌아야 할 횟수
    page_cnt = total_size // 10
    for idx in range(1):
        page_params = {
            "boardid": "notice",
            "sk": "",
            "sw": "",
            "category": "",
            "offset": 0 + idx * 10
        }
        response = requests.get(url, data=page_params)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.select(".board-list tbody tr")
        for row in rows:
            columns = row.select('td')
            types = "공지" if columns[0].get_text(strip=True) == "공지" else "일반"
            title = columns[1].get_text(strip=True)
            link = columns[1].select_one('a').get('href')
            writer = columns[2].get_text(strip=True)
            date = columns[3].get_text(strip=True)
            link = url + link
            board_data.append((title, link))
        
    return board_data
def fetch_nowongu_yntower() -> list:
    api_url = NOWONGU_YNTOWER_API_URL
    board_data = []

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': 'https://yntower.modoo.at/',
    }
    
    cnt = 8
    for p in range(1):
        params = {
            "cid": "a88etaku",
            "startNo": 1 + p*cnt,
            "count": cnt,
            "searchMode": 0,
            "replyAttr": 1
        }

        response = requests.post(api_url, data=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        length = len(response_data['messageList'])
        for i in range(length):
            img_list = []
            title = response_data['messageList'][i]['subject']
            writer = response_data['messageList'][i]['writer']
            img1 = response_data['messageList'][i]['image1']
            img2 = response_data['messageList'][i]['image2']
            img3 = response_data['messageList'][i]['image3']
            img4 = response_data['messageList'][i]['image4']
            img5 = response_data['messageList'][i]['image5']
            date = response_data['messageList'][i]['regTmStr']
            img_list.extend((img1, img2, img3, img4, img5))
            img_list = [img for img in img_list if len(img) > 0]
            board_data.append((title, img_list))
    return board_data

# =============================================================================================================

############################### 도봉구 사이트 ###############################
def fetch_dobongu_ssangmun() -> list:
    api_url = DOBONGU_SSANGMUN_URL_API
    board_data = []

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': 'https://eadgarssangmun.modoo.at/',
    }
    
    cnt = 8
    for p in range(1):
        params = {
            "cid": "qhovm1s8",
            "startNo": 1 + p*cnt,
            "count": cnt,
            "searchMode": 0,
            "replyAttr": 1
        }

        response = requests.post(api_url, data=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        length = len(response_data['messageList'])
        for i in range(length):
            img_list = []
            title = response_data['messageList'][i]['subject']
            writer = response_data['messageList'][i]['writer']
            content = response_data['messageList'][i]['content']
            img1 = response_data['messageList'][i]['image1']
            img2 = response_data['messageList'][i]['image2']
            img3 = response_data['messageList'][i]['image3']
            img4 = response_data['messageList'][i]['image4']
            img5 = response_data['messageList'][i]['image5']
            date = response_data['messageList'][i]['regTmStr']
            img_list.extend((img1, img2, img3, img4, img5))
            img_list = [img for img in img_list if len(img) > 0]

            board_data.append((title, img_list))
    return board_data
def fetch_dobongu_inhere() -> list:
    # URL 없음 / 입주 대기 불가
    pass

# =============================================================================================================

############################### 동대문구 사이트 ###############################
def fetch_dondaemungu_listana() -> list:
    url = DONGDAEMUNGU_LISTANAM_URL_API
    board_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
    params = {
        "code": 26
    }
    session = requests.Session()
    session.headers.update(headers)
    header_response = session.get(url, params=params, stream=True)
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select("#board_list tbody tr")
    for row in rows:
        datas = row.select('td')
        title = datas[1].get_text(strip=True)
        link = datas[1].select_one('a').get('href')
        try:
            file = datas[2].select_one('a').get('href')
        except:
            file = ""
        date = datas[3].get_text(strip=True)
        link = url + link
        board_data.append((title, link))
    return board_data
def fetch_dondaemungu_TRIUM() -> list:
    url = DONGDAEMUNGU_TRIUM_URL
    board_data = []
    
    headers = {
        'Content-Encoding':'gzip'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select(".board-list tbody tr")
    for row in rows:
        datas = row.select('td')
        types = datas[0].get_text(strip=True)
        link = datas[1].select_one('a').get('href')
        title = datas[1].get_text(strip=True)
        writer = datas[2].get_text(strip=True)
        date = datas[3].get_text(strip=True)
        link = url + link
        board_data.append((title, link))
    return board_data
def fetch_dondaemungu_hoegi() -> list:
    url = DONGDAEMUNGU_HOEGI_URL
    board_data = []

    header_response = requests.get(url, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select("#board_list tbody tr")
    for row in rows:
        datas = row.select('td')
        types = datas[0].get_text(strip=True)
        link = datas[1].select_one('a').get('href')
        title = datas[1].get_text(strip=True)
        try:
            file = datas[2].select_one('a').get('href')
        except:
            file = ""
        date = datas[3].get_text(strip=True)
        link = url + link
        board_data.append((title, link))
    return board_data
def fetch_dondaemungu_hkjsky() -> list:
    api_url = DONGDAEMUNGU_HKJSKY_URL_API
    board_data = []

    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': 'https://hkjskycity.modoo.at/',
    }
    cnt = 8
    for p in range(1):
        params = {
            "cid": "f3scs7qg",
            "startNo": 1 + p*cnt,
            "count": cnt,
            "searchMode": 0,
            "replyAttr": 1
        }

        response = requests.post(api_url, data=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        length = len(response_data['messageList'])
        for i in range(length):
            img_list = []
            title = response_data['messageList'][i]['subject']
            writer = response_data['messageList'][i]['writer']
            content = response_data['messageList'][i]['content']
            img1 = response_data['messageList'][i]['image1']
            img2 = response_data['messageList'][i]['image2']
            img3 = response_data['messageList'][i]['image3']
            img4 = response_data['messageList'][i]['image4']
            img5 = response_data['messageList'][i]['image5']
            date = response_data['messageList'][i]['regTmStr']
            img_list.extend((img1, img2, img3, img4, img5))
            img_list = [img for img in img_list if len(img) > 0]

            board_data.append((title, img_list))
    return board_data

# =============================================================================================================
