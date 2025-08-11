import json
from requests import Response

from discord import Message

from schema import ApplyhomeResponse


async def applyhome_response_handler(response: Response, message: Message):
    msg = ""
    for chunk in response.iter_lines():
        if chunk:
            chunk_str = chunk.decode()
            chunk_data = json.loads(chunk_str)
            chunk_data = ApplyhomeResponse(**chunk_data)

            event_state = chunk_data["event"]["state"]

            if event_state == "on_chat_model_stream":
                msg += chunk_data["content"]

                if len(msg) > 1000 and msg.endswith("\n\n"):
                    await message.channel.send(msg)
                    msg = ""

            elif event_state == "on_tool_start":
                tool_kwargs = chunk_data["tool_inputs"]
                tool_msg = "[SYSTEM] Tool 시작 "

                if tool_kwargs.get("types"):
                    tool_msg += f"**{tool_kwargs['types']}**의 최신 게시글들을 검색합니다. "
                    
                if tool_kwargs.get("jiyeok"):
                    tool_msg += f"**{tool_kwargs['jiyeok']}** 지역 내의 "
                    tool_msg += f"**{tool_kwargs['house_type']}** 유형의 공고문을 검색합니다."

                if tool_kwargs.get("question"):
                    tool_msg += f"**{tool_kwargs['question']}** 질문에 대한 답변을 "
                    tool_msg += f"**{tool_kwargs['pdf_url']}** 문서에 기반해서 생성합니다."

                await message.channel.send(tool_msg)

            elif event_state == "on_tool_end":
                # tool_msg = "[SYSTEM] 검색을 완료했습니다."
                tool_msg = "[SYSTEM] Tool 종료"
                await message.channel.send(tool_msg)

        else:
            # Stream End
            break
    
    await message.channel.send(msg)