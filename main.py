import os
import json
import firebase_admin
from firebase_admin import credentials, db
from telethon import TelegramClient, events

# 🔹 Load Firebase credentials from environment variable
firebase_json = os.getenv("FIREBASE_JSON")

if not firebase_json:
    raise ValueError("⚠️ FIREBASE_JSON environment variable is missing!")

# 🔹 Convert JSON string to dictionary
cred_dict = json.loads(firebase_json)

# 🔹 Initialize Firebase Admin SDK
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://your-project-id.firebaseio.com"
})

# 🔹 Telegram API credentials (Replace with your API details)
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# 🔹 Initialize Telegram Client
client = TelegramClient("session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🔹 Function to handle new messages
@client.on(events.NewMessage)
async def handler(event):
    message = event.message.message  # Get message text
    sender = await event.get_sender()  # Get sender details

    # 🔹 Store in Firebase
    ref = db.reference("messages")
    ref.push({
        "sender_id": sender.id,
        "sender_name": sender.username,
        "message": message
    })

    print(f"✅ Message stored: {message}")

# 🔹 Start the bot
print("🤖 Bot is running...")
client.run_until_disconnected()
