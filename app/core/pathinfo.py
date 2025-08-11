# 로그인 정보
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROMPT_TEMPLATE_DIR = BASE_DIR / ".." / "prompt_templates"

AGENT_DESCRIPTION_CONFIG = PROMPT_TEMPLATE_DIR.resolve() / "Agent_Description.yaml"
ROUTING_AGENT_CONFIG = PROMPT_TEMPLATE_DIR.resolve() / "Routing_Agent_Prompt.yaml"

USERNAME = ""
PASSWORD = ""

# ============================ 청년안심주택 공식 사이트 ============================
OFFICIAL_URL = "https://soco.seoul.go.kr/youth/bbs/BMSR00015/list.do?menuNo=400008"
OFFICIAL_URL_API = "https://soco.seoul.go.kr/youth/pgm/home/yohome/bbsListJson.json"
# ================================================================================

# ================================= 강남구 사이트 =================================
GANGNAMGU_LIST_URL = "http://www.listgangnam.co.kr/bbs/board.php?bo_table=news"
GANGNAMGU_LIST_API_URL = "http://www.listgangnam.co.kr/bbs/board.php?bo_table=news"

GANGNAMGU_THEONE_URL = "https://www.theoneys.co.kr/notice"
GANGNAMGU_THEONE_API_URL = "https://www.theoneys.co.kr/notice"

GANGNAMGU_ELGA_URL = "https://first-home.co.kr/board/index.html?id=notice"
GANGNAMGU_ELGA_API_URL = "https://first-home.co.kr/board/index.html?id=notice"

GANGNAMGU_MAESTRO_URL = "https://maestrosamseong.com/sub.php?code=26"
GANGNAMGU_MAESTRO_API_URL = "https://maestrosamseong.com/sub.php?code=26"

GANGNAMGU_DGSUMMIT_URL = "https://www.dg-summit.co.kr/24"
GANGNAMGU_DGSUMMIT_API_URL = "https://www.dg-summit.co.kr/24"


# ================================================================================

# ================================= 강동구 사이트 =================================
GANGDONGU_CHEONHO_URL = "http://xn--zf0bo4e9zsyre7pe70grdw68amqm.com/bbs/board.php?bo_table=notice"
GANGDONGU_CHEONHO_API_URL = "http://xn--zf0bo4e9zsyre7pe70grdw68amqm.com/bbs/board.php?bo_table=notice"

GANGDONGU_HYOSUNG_URL = "http://www.cheonho2030.com/sub/sub04_02.php"
GANGDONGU_HYOSUNG_API_URL = "http://www.cheonho2030.com/sub/sub04_02.php"

GANGONDGU_GILDONG_URL = "https://www.gildonglife.co.kr/Notice"
GANGONDGU_GILDONG_API_URL = "https://www.gildonglife.co.kr/Notice"
# ================================================================================

# ================================= 강북구 사이트 =================================
# 없음
# ================================================================================

# ================================= 강서구 사이트 =================================
GANGSEOGU_CENTERSQUAREBS_URL = "https://centersquarebs.com/420125488" # 센터스퀘어 발산
GANGSEOGU_CENTERSQUAREBS_API_URL = "https://centersquarebs.com/420125488" # 센터스퀘어 발산

GANGSEOGU_CENTERSQUARE_URL = "https://centersquare.modoo.at/?link=bpjvg4uq" # 센터스퀘어 등촌
GANGSEOGU_CENTERSQUARE_API_URL = "https://centersquare.modoo.at/apps/board/GetMessageList.json" # 센터스퀘어 등촌

GANGSEOGU_BONUM_URL = "https://bonumhaus2030.modoo.at/?link=czpnlnoj&page=1" # 보눔하우스
GANGSEOGU_BONUM_API_URL = "https://bonumhaus2030.modoo.at/apps/board/GetMessageList.json" # 보눔하우스

GANGSEOGU_FORTUNA_URL = "https://fortunablue.modoo.at/?link=dcn8otgl" # 포르투나 블루
GANGSEOGU_FORTUNA_API_URL = "https://fortunablue.modoo.at/apps/board/GetMessageList.json" # 포르투나 블루

GANGSEOGU_IM2030_URL = "https://im2030.modoo.at/?link=dv1398ka" # 아임2030
GANGSEOGU_IM2030_API_URL = "https://im2030.modoo.at/apps/board/GetMessageList.json" # 아임2030

GANGSEOGU_FLTOWER_URL = "https://fltower.modoo.at/?link=soo8sobp" # 아르체움
GANGSEOGU_FLTOWER_API_URL = "https://fltower.modoo.at/apps/board/GetMessageList.json" # 아르체움

GANGSEOGU_LCREW_URL = "https://youngtower.modoo.at/?link=94gu5os0" # 엘크루
GANGSEOGU_LCREW_API_URL = "https://youngtower.modoo.at/apps/board/GetMessageList.json" # 엘크루

GANGSEOGU_UJS_URL = "https://ujs2030.co.kr/sub06_1" # 해링턴타워
GANGSEOGU_UJS_API_URL = "https://ujs2030.co.kr/sub06_1" # 해링턴타워
# ================================================================================

# ================================= 관악구 사이트 =================================
GWANAKGU_BX201_URL = "https://bx201seoul.modoo.at/?link=3gs5oxwu"
GWANAKGU_BX201_URL_API = "https://bx201seoul.modoo.at/apps/board/GetMessageList.json"
GWANAKGU_SQUARE_URL = "https://centersquaresnu.com/sub/sub04_02.php"
GWANAKGU_CHOIGANG_URL = "https://www.xn--939aq02c7teiyd.com/sub/sub05_01.php?boardid=notice&sk=&sw=&category=&offset=0"
# ================================================================================

# ================================= 광진구 사이트 =================================
GWANGJINGU_CENTUM_URL = "http://www.centumhills.co.kr/bbs/board.php?bo_table=news"
GWANGJINGU_PODIUM_URL = "https://thepodium830.com/center/notice?isNotice=false&searchKey=all&searchValue&page=1"
GWANGJINGU_PODIUM_API_URL = "https://thepodium830.com/api/v1/center/notifications"
GWANGJINGU_PODIUM_DETAIL_URL = "https://thepodium830.com/center/notice/"
GWANGJINGU_VIVA_URL = "https://vivahillskb.co.kr/bbs/board.php?bo_table=notice"
GWANGJINGU_GUNJA = "https://remarkvillgunja.com/sub/sub04_02.php"
GWANGJINGU_GREENTOWER = "URL없음"
# ================================================================================

# ================================= 구로구 사이트 =================================
GUROGU_SEIZIUM_URL = "https://seizium-gb.com/center/notice?isNotice=false&searchKey=all&searchValue&page=1"
GUROGU_SEIZIUM_API_URL = "https://seizium-gb.com/api/v1/center/notifications?isNotice=false&searchKey=all"
# ================================================================================

# ================================= 금천구 사이트 =================================
# 없음
# ================================================================================

# ================================= 노원구 사이트 =================================
NOWONGU_INITIUM_URL = "https://mhinitium.co.kr/customer/index.php"
NOWONGU_YNTOWER_URL = "https://yntower.modoo.at/?link=a88etaku"
NOWONGU_YNTOWER_API_URL = "https://yntower.modoo.at/apps/board/GetMessageList.json"
# ================================================================================

# ================================= 도봉구 사이트 =================================
DOBONGU_SSANGMUN_URL = "https://eadgarssangmun.modoo.at/?link=qhovm1s8"
DOBONGU_SSANGMUN_URL_API = "https://eadgarssangmun.modoo.at/apps/board/GetMessageList.json"
DOBONGU_INHERE_URL = "URL 없음 / 입주 대기 불가"
# ================================================================================

# ================================= 동대문구 사이트 =================================
DONGDAEMUNGU_LISTANAM_URL = "https://www.listanam.co.kr/sub.php?code=26"
DONGDAEMUNGU_LISTANAM_URL_API = "https://www.listanam.co.kr/sub.php"
DONGDAEMUNGU_TRIUM_URL = "https://www.janganheartrium.co.kr/customer/notice.php"
DONGDAEMUNGU_HOEGI_URL = "https://www.doojin2030.co.kr/sub.php?code=10"
DONGDAEMUNGU_HOEGI_URL_API = "https://www.doojin2030.co.kr/sub.php"
DONGDAEMUNGU_HKJSKY_URL = "https://hkjskycity.modoo.at/?link=f3scs7qg"
DONGDAEMUNGU_HKJSKY_URL_API = "https://hkjskycity.modoo.at/apps/board/GetMessageList.json"
# ================================================================================

# ================================= 동작구 사이트 =================================
# DONGJAKGU_THECLASSIC_URL = "https://theclassic2030.modoo.at/?link=eez99qhu"
DONGJAKGU_THECLASSIC_URL = "https://theclassic2030.co.kr/24"
DONGJAKGU_THESUMMUIT_URL = "https://thesummittower.co.kr/24"

DONGJAKGU_COVE_URL = "http://sadang-cove.com/system/bbs/board.php?bo_table=notice"
DONGJAKGU_COVE_URL_API = "http://sadang-cove.com/system/bbs/board.php"

DONGJAKGU_GOLD_URL = "https://www.gold-tower.co.kr/customer/notice.php"
DONGJAKGU_NOBLESSE_URL = "https://www.db40314.kr/29"
# ================================================================================

# ================================= 마포구 사이트 =================================
MAPOGU_CREAONE_URL = "https://www.creaone.kr/kr/customer/notice.php"
MAPOGU_CREAONE_API_URL = "https://www.creaone.kr/kr/customer/notice.php"

MAPOGU_ELANDPEER_URL = "https://elandpeer.com/sinchon"
MAPOGU_ELANDPEER_API_URL = "https://elandpeer.com/sinchon"

MAPOGU_HYOSUNG_URL = "URL없음"
MAPOGU_HYOSUNG_API_URL = "URL없음"
# ================================================================================

# ================================= 서대문구 사이트 =================================
SEODAEMUNGU_URBANIEL_CHUNGJEONG_URL = "https://www.elyes.co.kr/info/noticeListAjax.do"
SEODAEMUNGU_STARTOWER_URL = "http://www.stkaja.co.kr/bbs/board.php?bo_table=news"
# ================================================================================

# ================================= 서초구 사이트 =================================
SEOCHOGU_FLOWER_URL = "https://seocho1502.modoo.at/?link=8a7g4ml6"
SEOCHOGU_CONEST_URL = "팝업형태로 모집공고 확인 가능"
# ================================================================================

# ================================= 성동구 사이트 =================================
SEONGDONGGU_HYSTAY_URL = "https://www.hy-stay.com/support/notice"
SEONGDONGGU_HYSTAY_API_URL = "https://www.hy-stay.com/support/notice?_rsc=1f6ho"

SEONGDONGGU_SAMJIN_URL = "https://blog.naver.com/sjumc00"
SEONGDONGGU_SAMJIN_API_URL = "https://blog.naver.com/PostList.naver?blogId=sjumc00&categoryNo=8&skinType=&skinId=&from=menu&userSelectMenu=true"


# ================================================================================

# ================================= 성북구 사이트 =================================
SEONGBUKGU_FELIX_URL = "https://felix222.com/center/notice?isNotice=false&searchKey=all&searchValue&page=1"
SEONGBUKGU_FELIX_API_URL = "https://felix222.com/api/v1/center/notifications?isNotice=false&searchKey=all"

SEONGBUKGU_JONGAM_URL = "https://xn--oi2ba973cqwhh4a78cwwcd18b.com/notice"
SEONGBUKGU_JONGAM_API_URL = "https://xn--oi2ba973cqwhh4a78cwwcd18b.com/notice"

# ================================================================================

# ================================= 송파구 사이트 =================================
SONGPAGU_CENTRAL_URL = "https://jamsilcentralpark.com/notice1"
SONGPAGU_CENTRAL_API_URL = "https://jamsilcentralpark.com/notice1"

SONGPAGU_JAMSILL_URL = "http://www.jamsilltower.co.kr/bbs/board.php?bo_table=5_1&sca=%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD"
SONGPAGU_JAMSILL_API_URL = "http://www.jamsilltower.co.kr/bbs/board.php?bo_table=5_1&sca=%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD"

SONGPAGU_MUNJEONG_MAESTRO_URL = "https://maestromunjeong.com/sub.php?code=26"
SONGPAGU_MUNJEONG_MAESTRO_API_URL = "https://maestromunjeong.com/sub.php?code=26"
# ================================================================================

# ================================= 양천구 사이트 =================================
# 없음
# ================================================================================

# ================================= 영등포구 사이트 =================================
YEONGDEUNGPOGU_FORENA_URL = "https://www.xn--910b48b70glxklhy.com/board/bbs/board.php?bo_table=notice"
YEONGDEUNGPOGU_FORENA_API_URL = "https://www.xn--910b48b70glxklhy.com/board/bbs/board.php?bo_table=notice"
# 영등포구 포레나 당산 --> Iframe 존재 / 외부 사이트("https://www.xn--910b48b70glxklhy.com/notice.html")

YEONGDEUNGPOGU_BRAVO_URL = "https://dorimbravo.modoo.at/?link=286i2ogk"
YEONGDEUNGPOGU_BRAVO_API_URL = "https://dorimbravo.modoo.at/apps/board/GetMessageList.json"

YEONGDEUNGPOGU_SINPUNG_URL = "https://sinpung2030.com/bbs/board.php?bo_table=notice"
YEONGDEUNGPOGU_SINPUNG_API_URL = "https://sinpung2030.com/bbs/board.php?bo_table=notice"

YEONGDEUNGPOGU_JUNTOWER_URL = "https://juntower.co.kr/service/notice"
YEONGDEUNGPOGU_JUNTOWER_API_URL = "https://juntower.co.kr/service/notice"
# ================================================================================

# ================================= 용산구 사이트 =================================
YONGSANGU_MAIN_URL = "https://ys-vertium-friends.co.kr/main/index.php"
YONGSANGU_LOGIN_URL = "https://ys-vertium-friends.co.kr/member/login_check.php"
YONGSANGU_BOARD_URL = "https://ys-vertium-friends.co.kr/board/board_list.php?board_name=508c75c8507"

YONGSANGU_LUMINI_URL = "https://www.elyes.co.kr/info/notice.do"
YONGSANGU_LUMINI_API_URL = "https://www.elyes.co.kr/info/noticeListAjax.do" # 신규 추가

YONGSANGU_LOTTECASTLE_URL = "https://www.elyes.co.kr/info/notice.do"
YONGSANGU_LOTTECASTLE_API_URL = "https://www.elyes.co.kr/info/noticeListAjax.do" # 신규 추가

YONGSANGU_URBANHUB25_URL = "https://www.urbanhub25.com/support/notice" # 신규 추가
YONGSANGU_URBANHUB25_API_URL = "https://www.urbanhub25.com/support/notice" # 신규 추가

# ================================================================================

# ================================= 은평구 사이트 =================================
EUNPYEONGU_GUSAN_URL = "https://duckyoung2016.com/notice" # 대기 희망자를 문자 지원으로 받고 있음 / 공지 X
EUNPYEONGU_GUSAN_API_URL = "https://duckyoung2016.com/notice" # 대기 희망자를 문자 지원으로 받고 있음 / 공지 X

EUNPYEONGU_VERITUM_URL = "https://xn--2z1bz6f6tctpw4vlsgid92d895c2hl.com/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/"
EUNPYEONGU_VERITUM_API_URL = "https://xn--2z1bz6f6tctpw4vlsgid92d895c2hl.com/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/"

EUNPYEONGU_LUMINO_URL = "https://lumino816.com/center/notice?isNotice=false&searchKey=all&searchValue&page=1"
EUNPYEONGU_LUMINO_API_URL = "https://lumino816.com/api/v1/center/notifications?isNotice=true"

EUNPYEONGU_LUCE_URL = "https://lucestation.com/sub/sub05_01.php"
EUNPYEONGU_LUCE_API_URL = "https://lucestation.com/sub/sub05_01.php"

EUNPYEONGU_STUDIO_URL = "https://www.thestudio163.co.kr/sub/sub05_01.php"
EUNPYEONGU_STUDIO_API_URL = "https://www.thestudio163.co.kr/sub/sub05_01.php"
# ================================================================================

# ================================= 종로구 사이트 =================================
JONGROGU_LOVENHEIM_URL = "https://www.lovenheim.imweb.me/notice1" # SSL 연결에 대한 무시 필요
JONGROGU_LOVENHEIM_API_URL = "https://www.lovenheim.imweb.me/notice1"

JONGROGU_DONGDAEMOONYONG_URL = "" # URL 없음
# ================================================================================

# ================================= 중구 사이트 =================================
JUNGGU_166TOWER_URL = "https://166tower.modoo.at/?link=5j8b3kfn"
JUNGGU_166TOWER_API_URL = "https://166tower.modoo.at/apps/board/GetMessageList.json"
# ================================================================================

# ================================= 중랑구 사이트 =================================
JUNGNANGU_JSTAR_URL = "https://jstar2030.modoo.at/?link=26i11qts"
JUNGNANGU_JSTAR_API_URL = "https://jstar2030.modoo.at/apps/board/GetMessageList.json"

JUNGNANGU_SBNPART_URL = "https://sbnpart.co.kr/center/notice.php"
JUNGNANGU_SBNPART_API_URL = "https://sbnpart.co.kr/center/notice.php"

JUNGNANGU_CARLTON_URL = "https://carltonterrace.modoo.at/?link=8pc68vsh"
JUNGNANGU_CARLTON_API_URL = "https://carltonterrace.modoo.at/apps/board/GetMessageList.json"
# ================================================================================

# ================================= LH / SH =================================
LH_SH_URL = "https://www.applyhome.co.kr/ai/aib/selectSubscrptCalender.do"
# ================================================================================
