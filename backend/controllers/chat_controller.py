from typing import Dict, Any

from fastapi import HTTPException
from db.chat_data import chat_data, chat_data_index
from Core.chatbot import MyChatBot


def get_chat_list():
    return [{"id": chat_id, "name": f"Chat {chat_id.replace('chat', '')}"} for chat_id in chat_data.keys()]

# Get chat messages by ID
def get_chat_history(chat_id: str):
    if chat_id not in chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat_data[chat_id]

# User sends a message (Fixed version)
async def user_sends_message(bot, chat_id: str, payload: Dict[Any, Any]):
    if chat_id not in chat_data:
        chat_data[chat_id] = []


    new_message_id = len(chat_data[chat_id]) + 1
    chat_data[chat_id].append({
        "id": new_message_id,
        "sender": payload['sender'],
        "message": payload['message']
    })

    # Bot auto-reply
    bot_reply = bot.generate(payload['message'])

    chat_data[chat_id].append(bot_reply)
    new_message_id = len(chat_data[chat_id]) + 1
    chat_data[chat_id].append({
        "id": new_message_id,
        "sender": "bot",
        "message": bot_reply
    })
    return bot_reply


# Create a new chat
def create_new_chat():
    index = chat_data_index[0]
    new_chat_id = f"chat{index}"
    chat_data_index[0]=index+1
    chat_data[new_chat_id] = []
    return {"id": new_chat_id, "name": f"Chat {index}"}

# Delete a chat
def delete_chat(chat_id: str):
    if chat_id not in chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")

    del chat_data[chat_id]
    return {"id": chat_id, "message": "Deleted Chat"}

