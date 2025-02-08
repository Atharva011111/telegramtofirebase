import os
import json
import firebase_admin
from firebase_admin import credentials, db
from telethon import TelegramClient, events
import re

# 🔹 Telegram API Details (Session File Use Karo)
api_id = 28320272  
api_hash = "bb6ca97823e0a07d86dfcef22746b4b7"  

# 🔹 Firebase Setup (Load from Environment Variable)
firebase_json = os.getenv("FIREBASE_JSON")  
if not firebase_json:
    raise ValueError("⚠️ FIREBASE_JSON environment variable is missing!")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://radarxtvscores-default-rtdb.firebaseio.com/"
})

# 🔹 Source Channel
source_channel = "RAdarxCricketline"  

# 🔹 Telegram Client (Session File Ka Use Karo)
client = TelegramClient("session_name", api_id, api_hash)  # ✅ No phone number required

async def main():
    await client.start()  # ✅ Session File Se Auto Login Hoga

    @client.on(events.NewMessage(chats=source_channel))
    async def store_message(event):
        message_text = event.message.text
        ref = db.reference("/telegram_messages")
        ref.child(str(event.message.id)).set({
            "text": message_text,
            "timestamp": event.message.date.timestamp()
        })

    @client.on(events.MessageDeleted(chats=source_channel))
    async def delete_message(event):
        ref = db.reference("/telegram_messages")
        ref.child(str(event.deleted_id)).delete()

    print("✅ Bot Running... Fetching New + Deleted Messages in REAL-TIME!")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())  # ✅ Auto-start without input()
