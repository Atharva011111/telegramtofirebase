from telethon import TelegramClient, events
import firebase_admin
from firebase_admin import credentials, db
import re

# 🔹 Telegram API Details
api_id = 28320272  
api_hash = 'bb6ca97823e0a07d86dfcef22746b4b7'  
phone_number = '+917319829261'  

# 🔹 Firebase Setup
cred = credentials.Certificate("C:/Users/Lenovo/Downloads/serviceAccountKey.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://radarxtvscores-default-rtdb.firebaseio.com/'  
})

# 🔹 Source Channel
source_channel = 'ALLROUNDERLINE'  

# 🔹 Telegram Client
client = TelegramClient('session_name', api_id, api_hash)

def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Emoticons
                               u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # Transport & map symbols
                               u"\U0001F700-\U0001F77F"  # Alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U00002702-\U000027B0"  # Dingbats
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)  # Emojis hata ke sirf text return karega

async def main():
    await client.start(phone_number)  

    @client.on(events.NewMessage(chats=source_channel))
    async def store_message(event):
        message_text = event.message.text  

        # 🔹 Emojis Remove Karna
        clean_text = remove_emojis(message_text).strip()

        # ✅ Agar clean text empty ho, toh ignore karna
        if not clean_text:
            return

        # ✅ Firebase me store karna
        ref = db.reference('/telegram_messages')  
        ref.push({
            'text': clean_text,
            'timestamp': event.message.date.timestamp()
        })

    print("✅ Bot chal raha hai... Purane + naye messages Firebase pe jaayenge.")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())