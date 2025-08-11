import os
import streamlit as st
import asyncio
import uuid
import requests
from urllib.parse import urljoin
from utils import build_routing_data
import handler
from save_chat import *

from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL')

APP_TITLE = "주택청약 공고"
APP_ICON = "🏡"  # 주택 아이콘
USER_ID_COOKIE = "user_id"

# 로그인 기능
if hasattr(st, "query_params"):
    login_user = st.query_params.get(USER_ID_COOKIE)
else:
    params = st.experimental_get_query_params()
    login_user = params.get(USER_ID_COOKIE, [None])[0]

# 있으면, 우하단 메세지 출력
if login_user:
    st.markdown(
        f"<div style='position:fixed; bottom:10px; right:10px; background:#e3f2fd; padding:8px 15px; border-radius:8px; color:#1976d2; z-index:10001;'>"
        f"🏡 반갑습니다. <b>{login_user}</b>님"
        "</div>",
        unsafe_allow_html=True
    )
else:
    st.error("로그인이 필요합니다.")
    st.stop()
    
# 세션 초기화
if "users" not in st.session_state:
    st.session_state["users"] = {}
if login_user not in st.session_state["users"]:
    st.session_state["users"][login_user] = load_user_data(login_user)
    
# 유저의 대화내용 저장
def save_now(login_user, users):
    save_user_data(login_user, users)
    
# thread 생성
def create_new_thread(user_ss):
    new_thread_id = str(uuid.uuid4())
    user_ss["threads"][new_thread_id] = []
    user_ss["current_thread"] = new_thread_id
    return new_thread_id

# 현재 쓰레드 세팅
def set_current_thread(user_ss, tid):
    user_ss["current_thread"] = tid

# 현재 쓰레드 불러오기
def get_current_thread_id(user_ss):
    return user_ss["current_thread"]

# 현재 쓰레드의 메시지 불러오기
def get_current_messages(user_ss):
    tid = get_current_thread_id(user_ss)
    if tid and tid in user_ss["threads"]:
        return user_ss["threads"][tid]
    return []

# 쓰레드 삭제 정보 담기
def set_delete_thread(user_ss, tid):
    user_ss["delete_thread"] = tid
    
# 쓰레드 삭제
def delete_thread(user_ss):
    tid = user_ss["delete_thread"]
    if tid in user_ss["threads"]:
        del user_ss["threads"][tid]
        # 만약 삭제 thread가 현 선택 thread일시, 새 thread 생성
        if user_ss["current_thread"] == tid:
            user_ss["current_thread"] = next(iter(user_ss["threads"]))
        else:
            create_new_thread(user_ss)
        user_ss["delete_thread"] = None

async def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        menu_items={},
    )

    # Hide the streamlit upper-right chrome
    st.html(
        """
        <style>
        [data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
            }
        </style>
        """,
    )
    if st.get_option("client.toolbarMode") != "minimal":
        st.set_option("client.toolbarMode", "minimal")
        await asyncio.sleep(0.1)
        st.rerun()
    
    users = st.session_state["users"][login_user]
    
    # 최초 1개 thread 자동 생성
    if not users["threads"]:
        create_new_thread(users)
    if not users["current_thread"]:
        users["current_thread"] = next(iter(users["threads"]))
    
    with st.sidebar:
        # 로그아웃
        if st.button("Logout", use_container_width=True):
            # 세션 정리시
            # st.session_state.clear()
            st.markdown(
                """
                <meta http-equiv="refresh" conent="0; url=http://localhost:3000/" />
                """,
                unsafe_allow_html=True
            )
            st.stop()

        
        st.header(f"{APP_ICON} {APP_TITLE}")
        # 1. 대화시작
        if st.button(":material/chat: New Chat", use_container_width=True):
            create_new_thread(users)
            st.rerun()
        
        # 2. 이전 세션 목록
        st.subheader("💾 History")
        for tid in list(users["threads"].keys()):
            msgs = users["threads"][tid]
            first_msg = "(빈 세션)" if not msgs else (msgs[0].get("content", "")[:8])
            display_name = login_user            
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                if st.button(f"{first_msg}({display_name})",
                             key=f"resume_{tid}",
                             use_container_width=True):
                    set_current_thread(users, tid)
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{tid}", use_container_width=True):
                    set_delete_thread(users, tid)

    # 3. thread 삭제
    if users["delete_thread"]:
        delete_thread(users)
        st.rerun()

    # 4. 이전 대화 불러오기
    messages = get_current_messages(users)
    for m in messages:
        role = m.get("role", "ai")
        content = m.get("content", "")
        st.chat_message(role).write(content)
    
    # 5-1.대화 시작
    if not messages:
        st.chat_message("ai").write("Hello I'm a bot!")
        
    # 5-2. 대화
    # 사용자 입력
    if user_input := st.chat_input("메세지를 입력하세요!"):
        user_msgs = {"role": "human", "content": user_input}
        users["threads"][get_current_thread_id(users)].append(user_msgs)
        st.chat_message("human").write(user_input)
        
        # agent의 응답
        # Routing 처리
        routing_data = build_routing_data(user_input, login_user, get_current_thread_id(users))
        routing_response = requests.post(
            urljoin(BACKEND_URL + "/", "routing_agent/invoke"),
            json=routing_data
        )
        if routing_response.status_code == requests.codes.ok:
            # 핸들링하는 로직 추가 필요
            response_data = routing_response.json()
            result_message = response_data.get("state", {}).get("response", "No response")
            agent_msgs = {"role": "ai", "content": result_message}
            users["threads"][get_current_thread_id(users)].append(agent_msgs)
            st.chat_message("ai").write(f"Routing result: {result_message}")
        else:
            st.chat_message("ai").write("Routing Agent 요청 실패")
    
if __name__ == "__main__":
    asyncio.run(main())
