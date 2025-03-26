from typing import Dict, Any
import pandas as pd
import io
from fastapi import HTTPException
from db.chat_data import chat_data, chat_data_index
from Core.chatbot import MyChatBot
import json


def get_chat_list():
    return [{"id": chat_id, "name": f"Chat {chat_id.replace('chat', '')}"} for chat_id in chat_data.keys()]

# Get chat messages by ID
def get_chat_history(chat_id: str):
    if chat_id not in chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat_data[chat_id]

# User sends a message (Fixed version)
async def user_sends_message(bot, chat_id: str, payload):
    if chat_id not in chat_data:
        chat_data[chat_id] = []

    new_message_id = len(chat_data[chat_id]) + 1
    user_message = {
        "id": new_message_id,
        "sender": payload["sender"],
        "message": payload["message"]
    }

    # ✅ Process CSV File if Uploaded
    if payload.get("file") and payload["file"].filename:  # Ensure file exists
        file = payload["file"]
        print(1)
        if file.filename.endswith(".csv"):
            print(2)
            contents = await file.read()
            df = pd.read_csv(io.BytesIO(contents))
            df = df.fillna("")  # Replace NaN with empty strin
            user_message["csv_preview"] = json.loads(df.head().to_json())  # Send first 5 rows as preview
        else:
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

    chat_data[chat_id].append(user_message)

    # ✅ Generate Bot Reply
    bot_reply = bot.generate(payload["message"])
    new_message_id = len(chat_data[chat_id]) + 1
    chat_data[chat_id].append({
        "id": new_message_id,
        "sender": "bot",
        "message": bot_reply
    })

    return {"user_message": user_message, "bot_reply": bot_reply}


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

