from contextlib import asynccontextmanager
from Core.chatbot import MyChatBot
from fastapi import APIRouter, FastAPI
from controllers.chat_controller import (
    get_chat_list,
    get_chat_history,
    user_sends_message,
    create_new_chat,
    delete_chat,
)

from typing import Dict, Any
@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' Run at startup
        Initialize the Client and add it to app.state
    '''
    app.state.chatbot = MyChatBot()
    yield
    ''' Run on shutdown
        Close the connection
        Clear variables and release the resources
    '''

app = FastAPI(lifespan=lifespan)

@app.get("/chats")
async def chats():
    return get_chat_list()

@app.get("/chats/{chat_id}")
async def chat_history(chat_id: str):
    return get_chat_history(chat_id)

@app.post("/chats/{chat_id}/send")
async def send_message(chat_id: str, payload: Dict[Any, Any]):
    return await user_sends_message(chat_id, payload)

@app.post("/chats")
async def new_chat():
    return create_new_chat()

@app.delete("/chats/{chat_id}")
async def remove_chat(chat_id: str):
    return delete_chat(chat_id)
