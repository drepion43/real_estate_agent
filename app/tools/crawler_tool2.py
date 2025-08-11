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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

############################### 동작구 사이트 ###############################

def fetch_dongjakgu_theclassic() -> list:
    url = DONGJAKGU_THECLASSIC_URL
    board_data = []
    # 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br"
    }

    header_response = requests.get(url, headers=headers, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select("ul.li_body.holder")
    for row in rows:
        title = row.select_one('.tit').get_text(strip=True)
        name = row.select_one('.name').get_text(strip=True)
        date = row.select_one('.time').get_text(strip=True)
        link = row.select_one('.tit').find("a", class_="list_text_title _fade_link").get('href')
        link = url + link
        board_data.append((title, link))
    return board_data
def fetch_dongjakgu_thesummit() -> list:
    url = DONGJAKGU_THESUMMUIT_URL
    board_data = []
    # 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br"
    }

    header_response = requests.get(url, headers=headers, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select("ul.li_body.holder")
    for row in rows:
        title = row.select_one('.tit').get_text(strip=True)
        name = row.select_one('.name').get_text(strip=True)
        date = row.select_one('.time').get_text(strip=True)
        link = row.select_one('.tit').find("a", class_="list_text_title _fade_link").get('href')
        link = url + link
        board_data.append((title, link))
    return board_data
def fetch_dongjakgu_cove() -> list:
    url = DONGJAKGU_COVE_URL
    board_data = []

    header_response = requests.get(url, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select("#fboardlist .bo_notice")
    for row in rows:
        types = row.select_one('.td_num').get_text(strip=True)
        title = row.select_one('.td_subject').get_text(strip=True)
        link = row.select_one('.td_subject a').get('href')
        writer = row.select_one('.td_name').get_text(strip=True)
        date = row.select_one('.td_date').get_text(strip=True)
        board_data.append((title, link))
    return board_data
def fetch_dongjakgu_gold() -> list:
    url = DONGJAKGU_GOLD_URL
    board_data = []

    header_response = requests.get(url, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select(".board-list tbody tr")
    for row in rows:
        datas = row.select('td')
        title = datas[1].get_text(strip=True)
        link = datas[1].select_one('a').get('href')
        writer = datas[2].get_text(strip=True)
        date = datas[3].get_text(strip=True)
        link = url + link
        board_data.append((title, link))
    return board_data
def fetch_dongjakgu_noblesse() -> list:
    url = DONGJAKGU_NOBLESSE_URL
    board_data = []
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    }
    
    header_response = requests.get(url, headers=headers, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select("ul.li_body.holder")
    for row in rows:
        title = row.select_one('.tit').get_text(strip=True)
        name = row.select_one('.name').get_text(strip=True)
        date = row.select_one('.time').get_text(strip=True)
        link = row.select_one('.tit').find("a", class_="list_text_title _fade_link").get('href')
        link = url + link
        board_data.append((title, link))
    return board_data

# =============================================================================================================

############################### 마포구 사이트 ###############################
def fetch_mapogu_creaone() -> list:
    url = MAPOGU_CREAONE_API_URL
    board_data = []

    header_response = requests.get(url, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select('.bbs-list-con li')
    for row in rows:
        title = row.select_one('.bbs-tit').get_text(strip=True)
        date = row.select_one('.bbs-date').get_text(strip=True)
        link = row.select_one('.bbs-list-item a').get('href')
        link = url + link
        board_data.append((title, link))
    return board_data
def fetch_mapogu_elandpeer() -> list:
    
    url = MAPOGU_ELANDPEER_API_URL
    board_data = []

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "https://soco.seoul.go.kr/",
            "Content-Type": "text/html; charset=utf-8",
            "Origin": "https://centersquare.modoo.at"
            }
    
    header_response = requests.get(url, headers=headers, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select('div.acd_group div.acd_row')
    for index, row in enumerate(rows):
        title = row.select_one('span.table-cell').get_text(strip=True)
        date = row.select_one('div.acd_collapse.collapse')
        date = date.attrs.get("data-code")
        date = date[1:9]
        board_data.append((title, date))
        
        print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    return board_data
def fetch_mapogu_hyosung() -> list:
    # URL 없음
    pass

# =============================================================================================================

############################### 서대문구 사이트 ###############################
def fetch_seodaemungu_urbaniel() -> list:
    url = SEODAEMUNGU_URBANIEL_CHUNGJEONG_URL
    keyword = "어바니엘 충정로"
    
    board_data = []

    header_response = requests.post(url, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select('table.table tbody tr')
    
    for index, row in enumerate(rows):
        title = row.select_one("td.tleft a").get_text(strip=True)
        datas = row.select('td')
        date = datas[-1].get_text(strip=True)
        
        # 특정 키워드 포함 여부 확인 후 필터링
        if keyword in title:
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")        
        
        print(f"{index + 1}. 제목: {title} | 날짜: {date}")
    return board_data
def fetch_seodaemungu_startower() -> list:
    url = SEODAEMUNGU_STARTOWER_URL
    board_data = []
    params = {
        "bo_table": "news",
        "page": 1,
    }

    header_response = requests.get(url, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    # print(soup)
    rows = soup.select('div.tbl_head01.tbl_wrap tbody tr')
    for row in rows:
        types = row.select_one('.td_num2').get_text(strip=True)
        title = row.select_one('.bo_tit').get_text(strip=True)
        link = row.select_one('.bo_tit a').get('href')
        writer = row.select_one('.td_name').get_text(strip=True)
        date = row.select_one('.td_datetime').get_text(strip=True)
        board_data.append((title, link))
    return board_data

# =============================================================================================================

############################### 서초구 사이트 ###############################
def fetch_seochogu_flower() -> list:
    api_url = SEOCHOGU_FLOWER_URL
    board_data = []
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': 'https://seocho1502.modoo.at/',
    }
    cnt = 8
    for p in range(1):
        params = {
            "cid": "8a7g4ml6",
            "startNo": 1 + p*cnt,
            "count": cnt,
            "searchMode": 0,
            "replyAttr": 1
        }

        response = requests.post(api_url, headers=headers, data=params)
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
def fetch_seochogu_conest() -> list:
    # 팝업 형태로 모집공고 확인 가능
    pass
# =============================================================================================================

############################### 성동구 사이트트 ###############################
def fetch_seongdonggu_hystay() -> list: # PASS, 
    pass
def fetch_seongdonggu_samjin() -> list: # PASS
    # 네이버블로그..?
    pass

# =============================================================================================================

############################### 성북구 사이트트 ###############################
def fetch_seongbukgu_felix() -> list: # JSON 형태, Header, Data 필요
    
    url = SEONGBUKGU_FELIX_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://felix222.com/center/notice?isNotice=false&searchKey=all&searchValue&page=1"
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
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_seongbukgu_jongam() -> list:
    
    url = SEONGBUKGU_JONGAM_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.li_board ul.li_body")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('li.tit a.list_text_title span').get_text(strip=True)
            date = data_list[index].select_one('li.time').get_text(strip=True)
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
# =============================================================================================================

############################### 송파구 사이트 ###############################
def fetch_songpagu_central() -> list: # HTML 형태, Header, 
    
    url = SONGPAGU_CENTRAL_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.li_table.row_04 div.acd_group div.acd_row")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one("span.table-cell").get_text(strip=True)
            date = data_list[index].select_one("div.date div").get_text(strip=True)

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_songpagu_munjeong_maestro() -> list: # PHP 형태, Header, Data 필요
    
    url = SONGPAGU_MUNJEONG_MAESTRO_API_URL

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        params = {
            "code": "26",
            }
        
        response = requests.get(url, headers=headers, data=params)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("table.table_board_basic tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('td.td_left a').get_text(strip=True)
            date = data_list[index].select('td')[-2].get_text(strip=True)
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_songpagu_jamsill() -> list: # PHP 형태, Data 필요 X
    
    url = SONGPAGU_JAMSILL_API_URL

    try:
        response = requests.get(url)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("ul.listWrap li.qa_li")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('div.question p.tit').get_text(strip=True)
            # date = data_list[index].select_one('td.td_datetime').get_text(strip=True)
            date = "날짜 없음/홈페이지 확인 필요"
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
# =============================================================================================================

############################### 양천구 사이트 ###############################

# =============================================================================================================

############################### 영등포구 사이트 ###############################
def fetch_yeongdeungpogu_forena() -> list: # HTML 형태, Header, 
    
    url = YEONGDEUNGPOGU_FORENA_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.tbl_head01.tbl_wrap table tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('td.td_subject a').get_text(strip=True)
            date = data_list[index].select_one('td.td_date').get_text(strip=True)

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_yeongdeungpogu_bravo() -> list: # GetmessageJson 형태
    
    url = YEONGDEUNGPOGU_BRAVO_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://dorimbravo.modoo.at/?link=286i2ogk",
            "Origin": "https://dorimbravo.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {
            "cid": "286i2ogk",     # 게시판 ID
            "startNo": 1,          # 몇 번째 글부터
            "count": 8,            # 몇 개 가져올지
            "searchMode": 0,       # 검색 여부 (0: 전체 목록, 그 외: 검색 조건 적용)
            "replyAttr": 1         # 글의 속성 필터링 (예: 댓글 포함 여부 등)
            }

        # POST 요청 보내기
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
def fetch_yeongdeungpogu_sinpung() -> list: # PHP 형태, Data 필요 X
    
    url = YEONGDEUNGPOGU_SINPUNG_URL

    try:
        response = requests.get(url)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.tbl_head01 table tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('div.bo_tit a').get_text(strip=True)
            date = data_list[index].select_one('td.td_datetime').get_text(strip=True)
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_yeongdeungpogu_juntower() -> list: # HTML 형태, Header, 
    
    url = YEONGDEUNGPOGU_JUNTOWER_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("table.table tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('td a').get_text(strip=True)
            date = data_list[index].select('td')[-1].get_text(strip=True)

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data

# =============================================================================================================

############################### 용산구 사이트 ###############################
def fetch_yongsangu_yongsan() -> list:
    
    board_data = []

    # 세션 생성
    session = requests.Session()

    # 로그인 요청 데이터 설정
    login_data = {
        "url":"",
        "member_id": os.getenv('YONGSAN_ID'),
        "member_password": os.getenv('YONGSAN_PASSWORD')
    }

    # 로그인 요청
    response = session.post(YONGSANGU_LOGIN_URL, data=login_data)
    response.raise_for_status()

    # 로그인 성공 확인
    if response.status_code != 200:
        raise Exception("로그인 실패")

    for p in range(1, 10):
        board_url = f'{YONGSANGU_BOARD_URL}&view_id=0&page={p}'
        # 게시판 페이지 요청
        response = session.get(board_url)
        response.raise_for_status()
        if response.status_code != 200:
            raise Exception("게시판 요청 실패")

        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.select("table.basic_board tbody tr.hover_list")

        for index, row in enumerate(rows):
            columns = row.find_all("td")
            if len(columns) > 3:
                title_element = columns[1].find("a")
                link_url = title_element["href"]
                title = title_element.text.strip()
                date = columns[3].text.strip()
                link = board_url + link_url[2:]
                board_data.append((title, link))
    
    return board_data
def fetch_yongsangu_lumini() -> list:
    url = YONGSANGU_LUMINI_API_URL
    keyword = "용산원효루미니"
    
    board_data = []

    header_response = requests.post(url, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select('table.table tbody tr')
    
    for index, row in enumerate(rows):
        title = row.select_one("td.tleft a").get_text(strip=True)
        datas = row.select('td')
        date = datas[-1].get_text(strip=True)
        
        # 특정 키워드 포함 여부 확인 후 필터링
        if keyword in title:
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")        
        
    return board_data
def fetch_yongsangu_lottecastle() -> list:
    url = YONGSANGU_LOTTECASTLE_API_URL
    keyword = "남영역 롯데캐슬"
    
    board_data = []

    header_response = requests.post(url, allow_redirects=False)
    header_response.raise_for_status()
    soup = BeautifulSoup(header_response.content, 'html.parser')
    rows = soup.select('table.table tbody tr')
    
    for index, row in enumerate(rows):
        title = row.select_one("td.tleft a").get_text(strip=True)
        datas = row.select('td')
        date = datas[-1].get_text(strip=True)
        
        # 특정 키워드 포함 여부 확인 후 필터링
        if keyword in title:
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")        
        
    return board_data
def fetch_yongsangu_urbanhub25() -> list: # 셀레니움 사용
    driver = configure_driver(ignore_ssl=False, ignore_certfi=False)
    result = fetch_board_urbanhub25(driver=driver)
    
    return result

# =============================================================================================================

############################### 은평구 사이트 ###############################
def fetch_eunpyeongu_vertium() -> list: # HTML 형태, Header, 
    
    url = EUNPYEONGU_VERITUM_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        response = requests.get(url, headers=headers)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.kboard-list table tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('div.kboard-default-cut-strings').get_text(strip=True)
            date = data_list[index].select_one('td.kboard-list-date').get_text(strip=True)

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_eunpyeongu_lumino() -> list: # Json 형태, Header, data 필요
    
    url = EUNPYEONGU_LUMINO_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "application/json, text/plain, */*",
            "referer": "https://lumino816.com/center/notice?isNotice=false&searchKey=all&searchValue&page=1",
            }
        
        params = {
            "isNotice": "true",
            }
        
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
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_eunpyeongu_luce() -> list: # PHP 형태, Data 필요 X
    
    url = EUNPYEONGU_LUCE_API_URL

    try:
        response = requests.get(url)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.board-list table tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('td.subject a').get_text(strip=True)
            date = data_list[index].select('td')[-1].get_text(strip=True)
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_eunpyeongu_studio() -> list: # PHP 형태, Data 필요 X
    
    url = EUNPYEONGU_STUDIO_API_URL

    try:
        response = requests.get(url)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.board-list table tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('td.subject a').get_text(strip=True)
            date = data_list[index].select('td')[-2].get_text(strip=True)
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_eunpyeongu_gusan() -> list: # 문자대기로 입주희망 받는중
    # 입주대기를 문자로 받고 있음
    msg = "입주대기를 문자로 받고 있음"
    return msg
# =============================================================================================================

############################### 종로구 사이트 ###############################
def fetch_jongrogu_lovenheim() -> list: # HTML 형태, Header, verify=False 필요 X
    
    url = JONGROGU_LOVENHEIM_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Referer": "https://www.lovenheim.imweb.me/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }
        
        response = requests.get(url, headers=headers, verify=False)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.acd_group div.acd_row")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('div.title div.tabled span.table-cell').get_text(strip=True)
            date = data_list[index].select_one('div.author div.date div').get_text(strip=True)
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_jongrogu_younghouse() -> list: # 홈페이지 없음
    msg = "별도의 홈페이지가 존재하지 않습니다. 청년안심주택 공식홈페이지에서 확인하세요."
    return msg
# =============================================================================================================

############################### 중구 사이트 ###############################
def fetch_junggu_166tower() -> list: # GetmessageJson 형태
    
    url = JUNGGU_166TOWER_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://166tower.modoo.at/?link=5j8b3kfn",
            "Origin": "https://166tower.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {
            "cid": "5j8b3kfn",     # 게시판 ID
            "startNo": 1,          # 몇 번째 글부터
            "count": 8,            # 몇 개 가져올지
            "searchMode": 0,       # 검색 여부 (0: 전체 목록, 그 외: 검색 조건 적용)
            "replyAttr": 1         # 글의 속성 필터링 (예: 댓글 포함 여부 등)
            }

        # POST 요청 보내기
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
# =============================================================================================================

############################### 중랑구 사이트 ###############################
def fetch_jungnangu_jstar() -> list: # GetmessageJson 형태
    
    url = JUNGNANGU_JSTAR_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://jstar2030.modoo.at/?link=26i11qts",
            "Origin": "https://jstar2030.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {
            "cid": "26i11qts",     # 게시판 ID
            "startNo": 1,          # 몇 번째 글부터
            "count": 8,            # 몇 개 가져올지
            "searchMode": 0,       # 검색 여부 (0: 전체 목록, 그 외: 검색 조건 적용)
            "replyAttr": 1         # 글의 속성 필터링 (예: 댓글 포함 여부 등)
            }

        # POST 요청 보내기
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
def fetch_jungnangu_sbnpart() -> list: # PHP 형태, Data 필요 X
    
    url = JUNGNANGU_SBNPART_API_URL

    try:
        response = requests.get(url)

        # 요청이 정상적으로 수행되지 않은 경우 예외 발생
        if response.status_code != 200:
            raise Exception(f"🚨 요청 실패: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data_list = soup.select("div.board-list table tbody tr")
    
        board_data = []
        for index in range(len(data_list)):
            title = data_list[index].select_one('td.subject a').get_text(strip=True)
            date = data_list[index].select('td')[-2].get_text(strip=True)
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    return board_data
def fetch_jungnangu_carlton() -> list: # GetmessageJson 형태
    
    url = JUNGNANGU_CARLTON_API_URL

    try:
        # 필수 요청 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://carltonterrace.modoo.at/?link=8pc68vsh&page=1",
            "Origin": "https://carltonterrace.modoo.at",
            "X-Requested-With": "XMLHttpRequest"
            }
        
        params = {
            "cid": "8pc68vsh",     # 게시판 ID
            "startNo": 1,          # 몇 번째 글부터
            "count": 8,            # 몇 개 가져올지
            "searchMode": 0,       # 검색 여부 (0: 전체 목록, 그 외: 검색 조건 적용)
            "replyAttr": 1         # 글의 속성 필터링 (예: 댓글 포함 여부 등)
            }

        # POST 요청 보내기
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
# =============================================================================================================
