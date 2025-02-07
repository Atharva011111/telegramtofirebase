import os
import json  # ✅ Fix: JSON module import kiya
import firebase_admin
from firebase_admin import credentials, db
from telethon import TelegramClient, events

# ✅ Firebase credentials ko Vercel ENV Variable se load kar
firebase_creds = json.loads(os.getenv("FIREBASE_CREDENTIALS"))  # 🔥 Fix Applied
cred = credentials.Certificate(firebase_creds)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://radarxtvscores-default-rtdb.firebaseio.com/'
})

# ✅ Telegram API Details
api_id = 28320272  
api_hash = 'bb6ca97823e0a07d86dfcef22746b4b7'  
phone_number = '+917319829261'  
source_channel = 'RadarXCricketLine'  

# ✅ Telegram Client
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone_number)  

    @client.on(events.NewMessage(chats=source_channel))
    async def store_message(event):
        message_text = event.message.text

        if message_text:
            # ✅ Firebase me store karna
            ref = db.reference('/telegram_messages')
            ref.push({
                'text': message_text,
                'timestamp': event.message.date.timestamp()
            })
            print(f"✅ Message Saved: {message_text}")

    print("🚀 Bot is Running on Vercel...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())