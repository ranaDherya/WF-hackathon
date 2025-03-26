import os
import zipfile
import pandas as pd
import io
from fastapi import HTTPException, Response

from Core.anomalydetection import run_anomaly_detection
from Core.codeexecution import code_execution
from Core.codegen import generate_rules
from db.chat_data import chat_data, chat_data_index
# from Core.chatbot import MyChatBot
import json
import concurrent.futures


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
    chat_data_index[0] = index + 1
    chat_data[new_chat_id] = []
    return {"id": new_chat_id, "name": f"Chat {index}"}


# Delete a chat
def delete_chat(chat_id: str):
    if chat_id not in chat_data:
        raise HTTPException(status_code=404, detail="Chat not found")

    del chat_data[chat_id]
    return {"id": chat_id, "message": "Deleted Chat"}


# Upload dataset
async def upload_dataset_csv(payload):
    user_message = {}
    # ✅ Process CSV File if Uploaded
    if payload.get("file") and payload["file"].filename:  # Ensure file exists
        file = payload["file"]
        print(1)
        if file.filename.endswith(".csv"):
            print(2)
            contents = await file.read()
            df = pd.read_csv(io.BytesIO(contents), skipinitialspace=True)
            df = df.fillna("")  # Replace NaN with empty strin
            try:
                os.remove("data/temp/data.zip")
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

            process_df(df)
            with zipfile.ZipFile("data/temp/data.zip", "w") as zip_file:
                for root, dirs, files in os.walk("data/temp"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, "data/temp"))

            headers = {"Content-Disposition": "attachment; filename=files.zip"}
            user_message["csv_preview"] = json.loads(df.head().to_json())  # Send first 5 rows as preview
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for root, dirs, files in os.walk("data/temp"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, "data/temp"))

            return Response(zip_buffer.getvalue(), headers=headers, media_type="application/zip")

        else:
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        # return {"message": "Uploaded Successfully"}


def generate_validation_report(df, columns):
    rules = generate_rules(columns)
    code_execution(rules, df)


def process_df(df):
    columns = list(df.columns)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_code_execution = executor.submit(generate_validation_report, df, columns)
        future_anomaly_detection = executor.submit(run_anomaly_detection, df)

    # Wait for both tasks to complete
    future_code_execution.result()
    future_anomaly_detection.result()
