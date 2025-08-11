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