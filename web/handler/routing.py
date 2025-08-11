import json

from requests import Response
import streamlit as st

from schema.routing import RoutingResponse

async def routing_response_handler(response: Response) -> str:
    """
    Routing Agent의 FastAPI 응답을 Streamlit에 출력하는 handler 함수.
    - stream 사용 여부 - X
    - 단일 JSON 객체 처리
    """
    # 응답 내용 디코드 및 파싱
    data = response.json()
    state_data = data.get("state", {})

    # Pydantic 검증
    routing_result = RoutingResponse(**state_data)

    # 시스템 메시지 표시
    st.chat_message("ai").write("[SYSTEM] 라우팅 결과를 수신했습니다.")

    # 라우팅 여부에 따른 응답
    if routing_result.isGuardpass:
        st.chat_message("ai").write(f"[SYSTEM] 해당 질문을 위해 **{routing_result.response}** 에이전트로 연결됩니다.")
    else:
        st.chat_message("ai").write(
            f"[SYSTEM] 입력하신 질문은 시스템 정책에 따라 처리할 수 없습니다: {routing_result.question}"
        )

    return routing_result.response