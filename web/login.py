import streamlit as st
import yaml
import bcrypt
import os

os.makedirs("/home/data/real_estate_agent/web/user_db", exist_ok=True)
USER_FILE = "/home/data/real_estate_agent/web/user_db/users.yaml"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("users", {})

def save_user(username, name, pw_hash):
    data = {}
    users = load_users()
    users[username] = {"name": name, "password": pw_hash.decode()}
    data["users"] = users
    with open(USER_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

def user_exists(username):
    users = load_users()
    return username in users

def verfity_user(username, password):
    users = load_users()
    if username in users:
        hashed = users[username]["password"].encode()
        return bcrypt.checkpw(password.encode(), hashed)
    return False

# streamlit UI
st.title("🏡 주택 공고 회원가입 및 로그인")

menu = st.sidebar.selectbox("페이지 선택", ["로그인", "회원가입"])

if menu == "회원가입":
    st.subheader("회원가입")
    new_username = st.text_input("아이디")
    new_name = st.text_input("이름")
    pw1 = st.text_input("비밀번호", type="password")
    pw2 = st.text_input("비밀번호 확인", type="password")
    if st.button("회원가입"):
        if not (new_username and new_name and pw1 and pw2):
            st.warning("모든 항목을 입력하세요.")
        elif user_exists(new_username):
            st.warning("이미 존재하는 아이디입니다.")
        elif pw1 != pw2:
            st.warning("비밀번호가 일치하지 않습니다.")
        else:
            pw_hash = bcrypt.hashpw(pw1.encode(), bcrypt.gensalt())
            save_user(new_username, new_name, pw_hash)
            st.success("회원가입이 완료되엇습니다! 로그인 해보세요.")
elif menu == "로그인":
    st.subheader("로그인")
    username = st.text_input("아이디")
    pw = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if verfity_user(username, pw):
            users = load_users()
            st.success(f"{users[username]["name"]}님 반갑습니다.")
            st.session_state["login_user"] = username
            
            # 리다이렉션
            st.markdown(f"""
                        <meta http-equiv="refresh" content="1;URL='http://localhost:8501?user_id={username}'" />
            """, unsafe_allow_html=True)
        else:
            st.error("아이디 혹은 비밀번호를 확인하세요.")
# 로그인 성공 로그
if "login_user" in st.session_state:
    users = load_users()
    l_user = st.session_state["login_user"]
    st.info(f"현재 로그인: {users[l_user]["name"]} ({l_user})")
    if st.button("로그아웃"):
        del st.session_state["login_user"]
        st.experimental_rerun()
