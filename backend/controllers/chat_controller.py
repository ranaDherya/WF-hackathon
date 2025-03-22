from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from db.chat_data import chat_data_index, chat_data 
from typing import Dict, Any

router = APIRouter()

# Define message input model
# class MessageInput(BaseModel):
#     sender: str
#     message: str

# Get list of available chats
@router.get("/chats")
def get_chat_list():
    return [{"id": chat_id, "name": f"Chat {chat_id.replace('chat', '')}"} for chat_id in chat_data.keys()]

# Get chat messages by ID
@router.get("/chats/{chat_id}")
def get_chat_history(chat_id: str):
    if chat_id not in chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat_data[chat_id]

# User sends a message (Fixed version)
@router.post("/chats/{chat_id}/send")
async def user_sends_message(chat_id: str, payload: Dict[Any, Any]):
    if chat_id not in chat_data:
        chat_data[chat_id] = []


    new_message_id = len(chat_data[chat_id]) + 1
    chat_data[chat_id].append({
        "id": new_message_id,
        "sender": payload['sender'],
        "message": payload['message']
    })


    # Bot auto-reply
    bot_reply = {
        "id": len(chat_data[chat_id]) + 1,
        "sender": "bot",
        "message": "This is a dummy response!"
    }
    chat_data[chat_id].append(bot_reply)

    return bot_reply


# Create a new chat
@router.post("/chats")
def create_new_chat(chat_data_index):
    index = chat_data_index[0]
    new_chat_id = f"chat{index}"
    chat_data_index[0]=index+1
    chat_data[new_chat_id] = []
    return {"id": new_chat_id, "name": f"Chat {index}"}

# Delete a chat
@router.delete("/chats/{chat_id}")
def delete_chat(chat_id: str):
    if chat_id not in chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")

    del chat_data[chat_id]
    return {"id": chat_id, "message": "Deleted Chat"}



