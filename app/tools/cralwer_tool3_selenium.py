import chromedriver_autoinstaller
import time
import sys
import os

# 현재 파일의 상위 디렉토리 경로를 찾기
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 상위 디렉토리에 있는 target_folder를 sys.path에 추가
sys.path.append(parent_dir)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.pathinfo import *

chromedriver_autoinstaller.install()

############################### Config Selenium Chrome driver ###############################
def configure_driver(ignore_ssl:bool, ignore_certfi:bool) -> webdriver.Chrome:
    options = Options()
    options.add_argument('--window-size= x, y')                 #실행되는 브라우저 크기를 지정할 수 있습니다.
    options.add_argument('--incognito')                         #시크릿 모드의 브라우저가 실행됩니다.
    options.add_argument('--headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
    
    # http일 경우에는 주석 처리 필요
    if (ignore_ssl == True):
        options.add_argument("--ignore-certificate-errors")         # SSL 인증 무시
        options.add_argument("--ignore-ssl-errors=yes")             # SSL 오류 무시

    return webdriver.Chrome(options=options)


############################### UTILITY FUNC ###############################
def pass_the_security_warning(driver: webdriver.Chrome) -> None:    
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
    try:
        focused_element = driver.switch_to.active_element
        element_text = focused_element.text.strip() if focused_element.text else "No Text"

        # 요소의 텍스트 리스트화 후 인덱스 찾기
        text_list = element_text.split("\n")
        try:
            target_index = text_list.index("사이트로 이동")
        except ValueError:
            print("버튼을 찾을 수 없습니다.")
            return

        # `Tab`을 target_index만큼 입력하여 이동 후 Enter 키 입력
        for _ in range(target_index):
            driver.switch_to.active_element.send_keys(Keys.TAB)
            time.sleep(0.1)

        driver.switch_to.active_element.send_keys(Keys.ENTER)
        
    except Exception as e:
        print(f"❌ 보안 경고 페이지 우회 실패: {e}")

############################### OFFICIAL SITE ###############################
def fetch_board_official(driver: webdriver.Chrome) -> list:
    
    url = OFFICIAL_URL
    try:
        driver.get(url)

        # Wait for the board list to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "boardList"))
        )

        # Extract board data
        rows = driver.find_elements(By.CSS_SELECTOR, "#boardList tr")
        board_data = []

        for index, row in enumerate(rows):
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 3:  # Ensure the row contains the expected columns
                title = columns[2].text.strip()
                date = columns[3].text.strip()
                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
                
    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### GANGNAM SITE ###############################
def fetch_board_list(driver: webdriver.Chrome) -> list:
    url = GANGNAM_LIST
    try:
        driver.get(url)
        pass_the_security_warning(driver=driver)
               
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr.bo_notice"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.td_subject div.bo_tit a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "span.gall_date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_elga(driver: webdriver.Chrome) -> list:
    
    url = GANGNAM_ELGA
    try:
        driver.get(url)

        # Wait for the list container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody#div_article_contents tr")))

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, 'tbody#div_article_contents tr:not([height="1"])')
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, 'td[align="left"] a')
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td:last-child")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_maestro(driver: webdriver.Chrome) -> list:
    
    url = GANGNAM_MAESTRO
    try:
        driver.get(url)

        # Wait for the list container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table[class^='table_board_basi'] tbody")))

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table[class^='table_board_basic'] tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, 'td.td_left a')
            title = title_element.text.strip()

            date_element = row.find_elements(By.CSS_SELECTOR, "td.mobile_x")[-1]
            date = date_element.text.strip()
            
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_theone(driver: webdriver.Chrome) -> list:
    
    url = GANGNAM_THEONE
    try:
        driver.get(url)

        # Wait for the list container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.li_body.holder")))

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, 'ul.li_body.holder')
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, 'a.list_text_title._fade_link')
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "li.time")
            date = date_element.get_attribute("title").strip()
            
            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### YONGSAN SITE ###############################
def fetch_board_yongsan(driver: webdriver.Chrome, username: str, password: str) -> list:

    main_url = YONGSANGU_MAIN_URL
    login_url = YONGSANGU_LOGIN_URL
    board_url = YONGSANGU_BOARD_URL
    
    try:
        # 로그인 페이지로 이동
        driver.get(login_url)

        # 로그인 정보 입력
        username_input = driver.find_element(By.NAME, "member_id")  # 사용자명 입력란
        password_input = driver.find_element(By.NAME, "member_password")  # 비밀번호 입력란
        login_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
            )

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        # 로그인 성공 확인 (URL 변경 기준)
        WebDriverWait(driver, 10).until(
            EC.url_to_be(main_url)
        )
        print("로그인 성공! \n현재 URL:", driver.current_url)

        # 특정 게시판 페이지로 이동
        driver.get(board_url)

        # 페이지 크롤링 (예: 게시글 제목 가져오기)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "sub_content"))  # 게시글 제목 클래스
        )
                
        # Extract board data
        rows = driver.find_elements(By.CSS_SELECTOR, "table.basic_board tbody tr.hover_list")
        board_data = []

        for index, row in enumerate(rows):
            # Extract columns (td elements)
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 3:
                title_element = columns[1].find_element(By.TAG_NAME, "a")
                title = title_element.text.strip()
                date = columns[3].text.strip()
                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생: ",e)

    finally:
        # 드라이버 종료
        driver.quit()

    return board_data
def fetch_board_lumini(driver: webdriver.Chrome) -> list:
    url = YONGSANGU_LUMINI_URL
    keyword = "용산원효루미니"
    
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.tleft a")
                title = title_element.text.strip()

                date_element = row.find_elements(By.CSS_SELECTOR, "td")
                date = date_element[-1].text.strip()
                
                # 특정 키워드 포함 여부 확인 후 필터링
                if keyword in title:
                    board_data.append((title, date))
                    print(f"{index + 1}. 제목: {title} | 날짜: {date}")

            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()
def fetch_board_urbanhub25(driver: webdriver.Chrome) -> list:
    url = YONGSANGU_URBANHUB25_URL
    
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.w-full.h-full.flex-col.justify-start.items-start.inline-flex a"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.w-full.h-full.flex-col.justify-start.items-start.inline-flex a")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "div.h-auto.grow.shrink div")
                title = title_element.text.strip()

                date_element = row.find_elements(By.CSS_SELECTOR, "div")
                date_element = date_element[7].get_attribute("textContent").strip()
                date = date_element
                
                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")

            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

############################### GANGDONG SITE ###############################
def fetch_board_cheonho(driver: webdriver.Chrome) -> list:
    url = GANGDONG_CHEONHO_URL
    try:
        driver.get(url)
        pass_the_security_warning(driver=driver)
               
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#bo_list tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "#bo_list tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.td_subject a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td.td_num")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_hyosung(driver: webdriver.Chrome) -> list:
    url = GANGDONG_HYOSUNG_URL
    try:
        driver.get(url)
        pass_the_security_warning(driver=driver)
               
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.news-list"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.news-list ul li")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "div.tit a")
                title = title_element.text.strip()

                # 게시글 날짜 추출
                try:
                    date_element = row.find_element(By.CSS_SELECTOR, "div.date")
                    date = date_element.text.strip()
                except:
                    date = "날짜 없음"

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_gildong(driver: webdriver.Chrome) -> list:
    url = GANGONDG_GILDONG_URL
    try:
        driver.get(url)
               
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.li_board"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "ul.li_body.holder, ul.li_body.notice_body.holder")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "a.list_text_title")
                title = title_element.text.strip()

                # 게시글 날짜 추출
                date_element = row.find_element(By.CSS_SELECTOR, "li.time")
                date = date_element.text.strip()
                
                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data


############################### GWANAKGU SITE ###############################
def fetch_board_bx201(driver: webdriver.Chrome) -> list:
    url = GWANAKGU_BX201_URL
    try:
        driver.get(url)

        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody._boardContent tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody._boardContent tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td div.area a.tit")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "span.date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_square(driver: webdriver.Chrome) -> list:
    url = GWANAKGU_SQUARE_URL
    try:
        driver.get(url)

        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.news-list"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.news-list ul li")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "div.tit a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "div.txt p")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_choigang(driver: webdriver.Chrome) -> list:
    url = GWANAKGU_CHOIGANG_URL
    try:
        driver.get(url)

        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.subject a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td")
                date = date_element[-2].text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### GWANGJINGU SITE ###############################
def fetch_board_centum(driver: webdriver.Chrome) -> list:
    url = GWANGJINGU_CENTUM_URL
    try:
        driver.get(url)
        
        pass_the_security_warning(driver=driver)
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr.bo_notice")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.td_subject div.bo_tit a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "span.gall_date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_podium(driver: webdriver.Chrome) -> list:
    url = GWANGJINGU_PODIUM_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.board-list tbody"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.board-list tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "div.ellip span")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td.board-list__txt")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_viva(driver: webdriver.Chrome) -> list:
    url = GWANGJINGU_VIVA_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tbl_head01 table tbody"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.tbl_head01 table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "div.bo_tit a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "span.gall_date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_gunja(driver: webdriver.Chrome) -> list:
    url = GWANGJINGU_GUNJA
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.notice-list ul"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.notice-list ul li")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "li div.tit")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "li div.date")
                date = date_element.text.strip()[2:]

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### NOWONGU SITE ###############################
def fetch_board_initium(driver: webdriver.Chrome) -> list:
    url = NOWONGU_INITIUM_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.board-list table"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.board-list table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.subject a")
                title = title_element.text.strip()

                date_element = row.find_elements(By.CSS_SELECTOR, "td")
                date = date_element[-2].text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_yntower(driver: webdriver.Chrome) -> list:
    url = NOWONGU_YNTOWER_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.result_notice table.table_type1"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.result_notice table.table_type1 tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "div.area a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "span.date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### DOBONGU SITE ###############################
def fetch_board_ssangmun(driver: webdriver.Chrome) -> list:
    url = DOBONGU_SSANGMUN_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_type1 tbody._boardContent"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_type1 tbody._boardContent tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td div.area a.tit")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td span.date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### DONGDAEMUNGU SITE ###############################
def fetch_board_listanam(driver: webdriver.Chrome) -> list:
    url = DONGDAEMUNGU_LISTANAM_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_board_basic tbody"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_board_basic tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.td_left a")
                title = title_element.text.strip()

                date_element = row.find_elements(By.CSS_SELECTOR, "td")
                date = date_element[-1].text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_trium(driver: webdriver.Chrome) -> list:
    url = DONGDAEMUNGU_TRIUM_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.subject a")
                title = title_element.text.strip()

                date_element = row.find_elements(By.CSS_SELECTOR, "td")
                date = date_element[-2].text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_hoegi(driver: webdriver.Chrome) -> list:
    url = DONGDAEMUNGU_HOEGI_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_board_basic tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_board_basic tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.td_left a")
                title = title_element.text.strip()

                date_element = row.find_elements(By.CSS_SELECTOR, "td")
                date = date_element[-1].text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_hkjsky(driver: webdriver.Chrome) -> list:
    url = DONGDAEMUNGU_HKJSKY_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_type1 tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_type1 tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td div.area a.tit")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td span.date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### DONGJAKGU SITE ###############################
def fetch_board_theclassic(driver: webdriver.Chrome) -> list:
    url = DONGJAKGU_THECLASSIC_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_type1 tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_type1 tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td div.area a.tit")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td span.date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_thesummit(driver: webdriver.Chrome) -> list:
    url = DONGJAKGU_THESUMMUIT_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.li_board ul.li_body"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.li_board ul.li_body")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "li.tit a.list_text_title span")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "li.time")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_cove(driver: webdriver.Chrome) -> list:
    url = DONGJAKGU_COVE_URL
    try:
        driver.get(url)
        pass_the_security_warning(driver=driver)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr.bo_notice")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.td_subject a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td.td_date")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_gold(driver: webdriver.Chrome) -> list:
    url = DONGJAKGU_GOLD_URL
    try:
        driver.get(url)
        pass_the_security_warning(driver=driver)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.board-list table tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.board-list table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.subject a")
                title = title_element.text.strip()

                date_element = row.find_elements(By.CSS_SELECTOR, "td")
                date = date_element[-2].text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_noblesse(driver: webdriver.Chrome) -> list:
    url = DONGJAKGU_NOBLESSE_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.li_board ul.li_body"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.li_board ul.li_body")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "li.tit a.list_text_title span")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "li.time")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### MAPOGU SITE ###############################
def fetch_board_creaone(driver: webdriver.Chrome) -> list:
    url = MAPOGU_CREAONE_URL
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.bbs-list-con ul.bbs-list-style04 li"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "article.bbs-list-con ul.bbs-list-style04 li")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "a div.bbs-list-style04-info p")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "span.bbs-date em")
                date = date_element.text.strip()

                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")
            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### SEODAEMUNGU SITE ###############################
def fetch_board_urbaniel_chungjeong(driver: webdriver.Chrome) -> list:
    url = SEODAEMUNGU_URBANIEL_CHUNGJEONG_URL
    keyword = "어바니엘 충정로"
    
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.tleft a")
                title = title_element.text.strip()

                date_element = row.find_elements(By.CSS_SELECTOR, "td")
                date = date_element[-1].text.strip()
                
                # 특정 키워드 포함 여부 확인 후 필터링
                if keyword in title:
                    board_data.append((title, date))
                    print(f"{index + 1}. 제목: {title} | 날짜: {date}")

            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_startower(driver: webdriver.Chrome) -> list:
    url = SEODAEMUNGU_STARTOWER_URL
    
    try:
        driver.get(url)
        pass_the_security_warning(driver=driver)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tbl_head01 table tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "div.tbl_head01 table tbody tr.bo_notice")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "div.bo_tit a")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "div.gall_info span.gall_date")
                date = date_element.text.strip()
                
                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")

            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### SEOCHOGU SITE ###############################
def fetch_board_flower(driver: webdriver.Chrome) -> list:
    url = SEOCHOGU_FLOWER_URL
    
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_type1 tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_type1 tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "div.area a.tit")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td span.date")
                date = date_element.text.strip()
                
                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")

            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### SEONGDONGU SITE ###############################

############################### SEONGBUKGU SITE ###############################
def fetch_board_felix(driver: webdriver.Chrome) -> list:
    url = SEONGBUKGU_FELIX_URL
    
    try:
        driver.get(url)
        
        # Wait for the table body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.board-list tbody tr"))
        )

        # Locate each row inside the table body
        rows = driver.find_elements(By.CSS_SELECTOR, "table.board-list tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.board-list__tit div span")
                title = title_element.text.strip()

                date_element = row.find_element(By.CSS_SELECTOR, "td.board-list__txt")
                date = date_element.text.strip()
                
                board_data.append((title, date))
                print(f"{index + 1}. 제목: {title} | 날짜: {date}")

            except Exception as e:
                print(f"Error extracting row {index + 1}: {e}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### SONGPA SITE ###############################
def fetch_board_central(driver: webdriver.Chrome) -> list:
    
    url = SONGPAGU_CENTRAL_URL
    try:
        driver.get(url)

        # Wait for the list container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.acd_group")))

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "div.li_table.row_04")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "span.table-cell")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "span[class*='date-cell']")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_munjeong_maestro(driver: webdriver.Chrome) -> list:
    
    url = SONGPAGU_MUNJEONG_MAESTRO_URL
    try:
        driver.get(url)

        # Wait for the list container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_board_basic tbody tr")))

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_board_basic tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "td.td_left a")
            title = title_element.text.strip()

            date_element = row.find_elements(By.CSS_SELECTOR, "td")
            date = date_element[-2].text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### YEONGDEUNGPOGU SITE ###############################
def fetch_board_forena(driver: webdriver.Chrome) -> list:
    
    url = YEONGDEUNGPOGU_FORENA_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.tbl_head01 table tbody")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "div.tbl_head01.tbl_wrap table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "td.td_subject a")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td.td_date")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_bravo(driver: webdriver.Chrome) -> list:
    
    url = YEONGDEUNGPOGU_BRAVO_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_type1 tbody")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_type1 tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "div.area a.tit")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td span.date")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_sinpung(driver: webdriver.Chrome) -> list:
    
    url = YEONGDEUNGPOGU_SINPUNG_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.tbl_head01 table tbody")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "div.tbl_head01 table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "div.bo_tit a")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td.td_datetime")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_juntower(driver: webdriver.Chrome) -> list:
    
    url = YEONGDEUNGPOGU_JUNTOWER_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "td a")
            title = title_element.text.strip()

            date_element = row.find_elements(By.CSS_SELECTOR, "td")
            date = date_element[-1].text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### EUNPYEONGU SITE ###############################
def fetch_board_vertium(driver: webdriver.Chrome) -> list:
    
    url = EUNPYEONGU_VERITUM_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.kboard-list table tbody")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "div.kboard-list table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "div.kboard-default-cut-strings")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td.kboard-list-date")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_lumino(driver: webdriver.Chrome) -> list:
    
    url = EUNPYEONGU_LUMINO_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.board-list tbody tr")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "table.board-list tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "div.ellip span")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td.board-list__txt")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_luce(driver: webdriver.Chrome) -> list:
    
    url = EUNPYEONGU_LUCE_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.board-list table tbody tr")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "div.board-list table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "td.subject a")
            title = title_element.text.strip()

            date_element = row.find_elements(By.CSS_SELECTOR, "td")
            date = date_element[-1].text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_studio(driver: webdriver.Chrome) -> list:
    
    url = EUNPYEONGU_STUDIO_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.board-list table tbody tr")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "div.board-list table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "td.subject a")
            title = title_element.text.strip()

            date_element = row.find_elements(By.CSS_SELECTOR, "td")
            date = date_element[-2].text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### JONGROGU SITE ###############################
def fetch_board_lovenheim(driver: webdriver.Chrome) -> list:
    
    url = JONGROGU_LOVENHEIM_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.acd_group div.acd_row")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "div.acd_group div.acd_row")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "div.title div.tabled span.table-cell")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "div.author div.date div")
            date = date_element.get_attribute("title")

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data


############################### JUNGGU SITE ###############################
def fetch_board_166tower(driver: webdriver.Chrome) -> list:
    
    url = JUNGGU_166TOWER_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_type1 tbody tr")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_type1 tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "div.area a.tit")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td span.date")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data

############################### JUNGNANGU SITE ###############################
def fetch_board_jstar(driver: webdriver.Chrome) -> list:
    
    url = JUNGNANGU_JSTAR_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_type1 tbody tr")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_type1 tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "div.area a.tit")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td span.date")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_sbnpart(driver: webdriver.Chrome) -> list:
    
    url = JUNGNANGU_SBNPART_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.board-list table tbody tr")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "div.board-list table tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "td.subject a")
            title = title_element.text.strip()

            date_element = row.find_elements(By.CSS_SELECTOR, "td")
            date = date_element[-2].text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data
def fetch_board_carlton(driver: webdriver.Chrome) -> list:
    
    url = JUNGNANGU_CARLTON_URL
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table_type1 tbody tr")))
        

        # Locate each post item inside the board list
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table_type1 tbody tr")
        board_data = []

        for index, row in enumerate(rows):
            title_element = row.find_element(By.CSS_SELECTOR, "div.area a.tit")
            title = title_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td span.date")
            date = date_element.text.strip()

            board_data.append((title, date))
            print(f"{index + 1}. 제목: {title} | 날짜: {date}")

    except Exception as e:
        print("오류 발생:", e)

    finally:
        # WebDriver 종료
        driver.quit()

    return board_data






# options.add_argument('--headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
# options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
# options.add_argument('--mute-audio')                      #브라우저에 음소거 옵션을 적용합니다.

# options.set_capability("acceptInsecureCerts", True)       # SSL 인증서 오류 무시
# options.add_argument("--test-type")                       # 보안 경고 페이지 비활성화
# options.add_argument('--disable-blink-features=AutomationControlled') #시크릿 모드의 브라우저가 실행됩니다.
    
# options.add_argument("--allow-running-insecure-content")                      # 보안 경고 무시
# options.add_argument("--allow-insecure-localhost")                            # 보안되지 않은 로컬 서버(HTTPS 인증서 오류가 있는 서버) 허용


# options.add_argument("--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost")  # HTTPS 자동 변경 방지
# options.add_argument("--disable-web-security")            # 보안 설정 해제
# options.add_argument('--start-maximized')                 #브라우저가 최대화된 상태로 실행됩니다.
# options.add_argument('--start-fullscreen')                #브라우저가 풀스크린 모드(F11)로 실행됩니다.