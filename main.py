import os
import json
import firebase_admin
from firebase_admin import credentials, db
from telethon import TelegramClient, events
import re

# 🔹 Telegram API Details (Directly Hardcoded)
api_id = 28320272  
api_hash = "bb6ca97823e0a07d86dfcef22746b4b7"  
phone_number = "+917319829261"  

# 🔹 Load Firebase credentials from environment variable
firebase_json = os.getenv("FIREBASE_JSON")  # 🔹 JSON as an env variable
if not firebase_json:
    raise ValueError("⚠️ FIREBASE_JSON environment variable is missing!")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://radarxtvscores-default-rtdb.firebaseio.com/"
})

# 🔹 Source Channel
source_channel = "RAdarxCricketline"  

# 🔹 Telegram Client
client = TelegramClient("session_name", api_id, api_hash)

# 🔹 Remove Emojis Function
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub("", text)

async def main():
    await client.start(phone_number)

    # ✅ New Message Listener
    @client.on(events.NewMessage(chats=source_channel))
    async def store_message(event):
        message_text = event.message.text
        clean_text = remove_emojis(message_text).strip()
        if not clean_text:
            return

        # ✅ Store in Firebase
        ref = db.reference("/telegram_messages")
        ref.child(str(event.message.id)).set({
            "text": clean_text,
            "timestamp": event.message.date.timestamp()
        })

    # ✅ Message Delete Listener
    @client.on(events.MessageDeleted(chats=source_channel))
    async def delete_message(event):
        ref = db.reference("/telegram_messages")
        ref.child(str(event.deleted_id)).delete()

    print("✅ Bot Running... Fetching New + Deleted Messages in REAL-TIME!")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
