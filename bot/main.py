import os, requests
import handler
import discord

from discord import Message
from dotenv import load_dotenv
from urllib.parse import urljoin
from utils import build_json_data, build_routing_data, convert_routing_to_payload


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')

intents = discord.Intents().default()
intents.message_content = True

client = discord.Client(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"Hello {client.user.name}")


@client.event
async def on_message(message: Message):
    files = []
    if message.author == client.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type == 'application/pdf':
                file_path = os.path.join('downloads', attachment.filename)
                file = await attachment.read()
                files.append(file_path)

                response = requests.post(
                    url=urljoin(BACKEND_URL + "/", "pdf_agent/uploadfiles"),
                    files={"file": (attachment.filename, file)}
                )

                if response.status_code != requests.codes.ok:
                    await message.channel.send(f"PDF 업로드 실패: {attachment.filename}")
                    return
                else:
                    await message.channel.send(f"PDF 내용 검토 중... [{attachment.filename}]")
            else:
                await message.channel.send("지원하지 않는 파일 형식입니다. PDF 파일만 지원됩니다.")
                return

    # ✅ 파일이 있든 없든 routing_agent 호출
    # await message.channel.send("[SYSTEM] 사용자 질문을 분석 중...")
    # routing_resp = requests.post(
    #     url=urljoin(BACKEND_URL + "/", "routing_agent/invoke"),
    #     json=build_routing_data(message, pdf_paths=files)
    # )
    
    # if routing_resp.status_code != requests.codes.ok:
    #     await message.channel.send("[ERROR] Routing Agent 요청 실패")
    #     return
# ======================================= Routing Agent =======================================

    
    if message.content.startswith("/"):
        # Routing 처리
        await message.channel.send("[SYSTEM] 사용자 질문을 입력 받았습니다.")
        routing_resp = requests.post(
            url = urljoin(BACKEND_URL + "/", "routing_agent/invoke"),
            json=build_routing_data(message)
        )

        print("🚨 Routing Response:", routing_resp.status_code)
        print("🚨 Routing Body:", routing_resp.text)
        # 2. 응답이 정상인 경우, 핸들러 함수 호출
        if routing_resp.status_code == requests.codes.ok:
            await handler.routing_response_handler(routing_resp, message)
            
        else:
            await message.channel.send("[ERROR] Routing Agent 요청 실패")
            return
        
        routing_data = routing_resp.json()
        state = routing_data.get("state", {})
        config = routing_data.get("config", {})
        agent_type = state.get("response", "")
        
        # PDF Agent 분기
        if agent_type == "pdf_agent":
            pdf_payload = convert_routing_to_payload(state, config, message)
            response = requests.post(
                url = urljoin(BACKEND_URL + "/", "pdf_agent/astream"),
                json=pdf_payload,
                stream=True,
            )
            if response.status_code == requests.codes.ok:
                await handler.pdf_response_handler(response, message)
            else:
                raise Exception("Error")


        # applyhome Agent 분기
        elif agent_type == "applyhome_agent":
            print("Applyhome Agent 진입")
            applyhome_payload = convert_routing_to_payload(state, config, message)
            print("Applyhome agent payload : ", applyhome_payload)
            response = requests.post(
                url = urljoin(BACKEND_URL + "/", "applyhome_agent/astream"),
                json=applyhome_payload,
                stream=True
            )
                
            if response.status_code == requests.codes.ok:
                await handler.applyhome_response_handler(response, message)
            else:
                raise Exception("Error")
        
        # law agent 분기
        elif agent_type == "law_agent":
            print("Law Agent 진입")
            law_payload = convert_routing_to_payload(state, config, message)
            print("Law agent payload : ", law_payload)
            response = requests.post(
                url = urljoin(BACKEND_URL + "/", "law_agent/astream"),
                json=law_payload,
                stream=True
            )
            
            if response.status_code == requests.codes.ok:
                await handler.law_response_handler(response, message)
            else:
                raise Exception("Error")
# =============================================================================================
    if message.content.startswith("/applyhome"):
        
        response = requests.post(
            # url=os.path.join(BACKEND_URL, "applyhome_agent", "astream"),
            url=BACKEND_URL + "/applyhome_agent/astream",
            json=build_json_data(message, "/applyhome"),
            stream=True
        )

        if response.status_code == requests.codes.ok:
            await handler.applyhome_response_handler(response, message)
        else:
            raise Exception("Error")

    if message.content.startswith("/pdf"):
        data = build_json_data(message, "/pdf")
        data["config"].update({"pdf_path": []})
        response = requests.post(
            url=os.path.join(BACKEND_URL, "pdf_agent", "astream"),
            json=data,
            stream=True,
        )
        if response.status_code == requests.codes.ok:
            await handler.pdf_response_handler(response, message)
        else:
            raise Exception("Error")
        
################################################# test law ######################
    if message.content.startswith("/law"):
        print("law agent 진입")
        
        response = requests.post(
            url=BACKEND_URL + "/law_agent/astream",
            json=build_json_data(message, "/law"),
            stream=True
        )

        if response.status_code == requests.codes.ok:
            await handler.law_response_handler(response, message)
        else:
            raise Exception("Error")

client.run(TOKEN)
