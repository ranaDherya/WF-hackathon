from contextlib import asynccontextmanager
# from Core.chatbot import MyChatBot
from fastapi import APIRouter, FastAPI, Request, Form, File, UploadFile, Depends
from controllers.chat_controller import (
    get_chat_list,
    get_chat_history,
    user_sends_message,
    create_new_chat,
    delete_chat,
    upload_dataset_csv,
)
# from Core.utility import getApiKey
from typing import Dict, Any, Optional

router = APIRouter()

@router.get("/chats")
async def chats():
    return get_chat_list()

@router.get("/chats/{chat_id}")
async def chat_history(chat_id: str):
    return get_chat_history(chat_id)

@router.post("/chats/{chat_id}/send")
async def send_message(
    request: Request,
    chat_id: str,
    message: str = Form(...),
):
    payload = {"sender": "user", "message": message}
    return await user_sends_message(request.app.state.chatbot, chat_id, payload)
@router.post("/chats")
async def new_chat():
    return create_new_chat()

@router.delete("/chats/{chat_id}")
async def remove_chat(chat_id: str):
    return delete_chat(chat_id)

@router.post("/dataset")
async def upload_dataset(file: UploadFile):
    payload = {"file": file}
    return await upload_dataset_csv(payload)
