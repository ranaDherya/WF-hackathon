from fastapi import APIRouter, HTTPException, Request
from controllers.chat_controller import (
    get_chat_list,
    get_chat_history,
    user_sends_message,
    create_new_chat,
    delete_chat,
)
from db.chat_data import chat_data_index
from typing import Dict, Any

router = APIRouter()

@router.get("/chats")
async def chats():
    return get_chat_list()

@router.get("/chats/{chat_id}")
async def chat_history(chat_id: str):
    return get_chat_history(chat_id)

@router.post("/chats/{chat_id}/send")
async def send_message(chat_id: str, payload: Dict[Any, Any]):
    return await user_sends_message(chat_id, payload)

@router.post("/chats")
async def new_chat():
    return create_new_chat(chat_data_index)

@router.delete("/chats/{chat_id}")
async def remove_chat(chat_id: str):
    return delete_chat(chat_id)
