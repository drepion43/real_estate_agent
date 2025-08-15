import json
from requests import Response
import streamlit as st

from schema import PDFResponse

def pdf_response_handler(response: Response, users_history: list):
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
                    st.chat_message("ai").write(msg)
                    msg = ""

            elif event_state == "on_tool_start":
                tool_kwargs = chunk_data["tool_inputs"]
                tool_msg = "[SYSTEM] "
                tool_msg += f"**{tool_kwargs['question']}**에 연관한 내용을 확인하는 중입니다."
                tool_msg += f"**확인중인 공고 링크는 {tool_kwargs['announcement_link']}**입니다."
                st.chat_message("ai").write(tool_msg)
                agent_msgs = {"role": "ai", "content": tool_msg}
                users_history.append(agent_msgs)
            elif event_state == "on_tool_end":
                tool_msg = "[SYSTEM] 내용 확인을 완료했습니다."
                st.chat_message("ai").write(tool_msg)
                agent_msgs = {"role": "ai", "content": tool_msg}
                users_history.append(agent_msgs)
        else:
            break
    st.chat_message("ai").write(msg)
    agent_msgs = {"role": "ai", "content": msg}
    users_history.append(agent_msgs)
    return msg
