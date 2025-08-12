def build_routing_data(message: str, user_id, thread_id) -> dict:
    print(message, user_id, thread_id)
    data = {
        "state": {
            "question": message,  # "/청약 알려줘" → "청약 알려줘"
            "response": "",
            "isGuardpass": False
        },
        "config": {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            },
            "config": {}
        }
    }
    return data

def routing_to_payload(state: dict, user_id: str, thread_id: str) -> dict:
    data = {
        "state": {
            "messages": [
                {
                    "type": "human",
                    "content": state.get("question", "")
                }
            ],
            "is_last_step": False,
            "remaining_steps": 10
        },
        "config": {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id
            }
        }
    }
    return data