import json

from requests import Response
from discord import Message

from schema.routing import RoutingResponse

async def routing_response_handler(response: Response, message: Message):
    """
    Routing Agent의 FastAPI 응답을 Discord에 출력하는 handler 함수.
    - stream 사용 여부 - X 
    -단일 JSON 객체 처리
    """
    # 응답 내용 디코드 및 파싱
    data = response.json()
    state_data = data.get("state", {})

    # Pydantic 검증
    routing_result = RoutingResponse(**state_data)

    # 시스템 메시지 전송
    await message.channel.send("[SYSTEM] 라우팅 결과를 수신했습니다.")

    # 라우팅 여부에 따른 응답
    if routing_result.isGuardpass:
        await message.channel.send(f"[SYSTEM] 해당 질문을 위해 **{routing_result.response}** 에이전트로 연결됩니다.")
    else:
        await message.channel.send(f"[SYSTEM] 입력하신 질문은 시스템 정책에 따라 처리할 수 없습니다: {routing_result.question}")

    # PDF 정보가 있다면 출력
    # if routing_result.pdf_info:
    #     await message.channel.send(f"📎 관련 PDF 파일 수: {len(routing_result.pdf_info)}")
    #     await message.channel.send("\n".join(routing_result.pdf_info))
        
    return routing_result.response