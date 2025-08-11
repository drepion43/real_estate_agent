import json
from requests import Response

from discord import Message

from schema import PDFResponse

async def pdf_response_handler(response: Response, message: Message):
    msg = ""
    for chunk in response.iter_lines():

        if chunk:
            chunk_str = chunk.decode()
            chunk_data = json.loads(chunk_str)
            chunk_data = PDFResponse(**chunk_data)

            event_state = chunk_data["event"]["state"]

            if event_state == "on_chat_model_stream":
                msg += chunk_data["content"]
                if len(msg) > 1000 and msg.endswith("\n\n"):
                    await message.channel.send(msg)
                    msg = ""

            elif event_state == "on_tool_start":
                tool_kwargs = chunk_data["tool_inputs"]
                tool_msg = "[SYSTEM] "
                tool_msg += f"**{tool_kwargs['question']}**에 연관한 내용을 확인하는 중입니다."
                tool_msg += f"**확인중인 공고 링크는 {tool_kwargs['announcement_link']}**입니다."
                await message.channel.send(tool_msg)

            elif event_state == "on_tool_end":
                tool_msg = "[SYSTEM] 내용 확인을 완료했습니다."
                await message.channel.send(tool_msg)

        else:
            break

    await message.channel.send(msg)
