from discord import Message


def build_json_data(message: Message, command: str = None) -> dict:
    if command is not None:
        content = message.content.split(command)[-1].lstrip()
    else:
        content = message.content
    data = {
        "state": {
            "messages": [
                {
                    "type": "human",
                    "content": content,
                }
            ],
            "is_last_step": False,
            "remaining_steps": 10,
        },
        "config": {
            "configurable": {
                "thread_id": message.author.name,
                "user_id": message.author.id,
            }
        },
    }
    return data

def convert_routing_to_payload(state: dict, config: dict, message: Message) -> dict:
    data =  {
        "state": {
            "messages": [
                {
                    "type": "human", 
                    "content": state.get("question", "")
                }
            ],
            "is_last_step": False,
            "remaining_steps": 10,
        },
        "config": {
            "configurable": {
                "thread_id": message.author.name,
                "user_id": message.author.id,
            }
        },
    }
    return data


def build_routing_data(
    message: Message, 
    # pdf_paths: list[str] = []
) -> dict:
    data = {
        "state": {
            "question": message.content.lstrip("/"),  # "/청약 알려줘" → "청약 알려줘"
            "response": "",
            "isGuardpass": False
        },
        "config": {
            "configurable": {
                "thread_id": message.author.name,
                "user_id": message.author.id,
            },
            "config": {}
        }
    }
    return data