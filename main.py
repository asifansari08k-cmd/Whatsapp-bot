from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from flask import Flask
from threading import Thread
import asyncio

# --- WEB SERVER FOR RENDER (Keep Alive) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Running Live!"

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

# --- AAPKE DETAILS ---
API_ID = 37314366
API_HASH = "bd4c934697e7e91942ac911a5a287b46"
STRING_SESSION = "AQI5Xz4ASE6O7locP7_vLrorMTsXT3u80PL1M3tt20Ty8FavBKQdfbZOWjQFyai9DI46XwNhspJZO7S-V7X9JigDkGjAIfF9swyWqmvkRm1uxxR3ajE9rc4IueYDhBY60CeGk_S0FdD9IAQDmjiycLIOAI4PEvKrP5wi-5i6ecZCz4gxbpmyX5o-S8JnVfv51kivPaXVN3ioFP_TB01cgH29aJ9Oa7axnPKlTaq7hadmFfVEttBthtiT2rLz9QkX9CYmEaCJHopr8W1NqR9Is9VOPo6Y2HUGu_kh8mT1y3mgUswR_942rVYYvX43HQuq2wh1zvkf70PbVl89-2DTVHsKLrv9qQAAAAHxiovLAA"

# --- CONFIGURATION ---
SOURCE_CHANNEL = "Junaidniz" 
DESTINATIONS = ["otpMgroup"] 

# OTP Forwarder Settings
OTP_SOURCE = -1003087662000
OTP_DEST = "otpMgroup"
TARGET_BOTS = ["junaidaliRebot", "JunaidnnRebot"]

app = Client("GourisenMegaBot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# --- FEATURE 1: OTP FORWARDER ---
@app.on_message(filters.chat(OTP_SOURCE))
async def otp_logic(client, message):
    sender = message.from_user.username if message.from_user else ""
    if sender in TARGET_BOTS:
        text = message.text or message.caption
        if text:
            # Credit hatana
            clean_text = text.split("Powered By")[0].strip() if "Powered By" in text else text.strip()
            # Quote + Branding
            final_msg = f"<blockquote>{clean_text}</blockquote>\n⚡ Powered by Gourisen OSINT"
            
            try:
                await client.send_message(
                    chat_id=OTP_DEST, 
                    text=final_msg,
                    parse_mode=ParseMode.HTML
                )
                print(f"✅ OTP Bhej Diya!")
            except Exception as e:
                print(f"❌ OTP Error: {e}")

# --- FEATURE 2: FILE CLONER ---
@app.on_message(filters.chat(SOURCE_CHANNEL) & (filters.document | filters.video | filters.audio | filters.photo))
async def file_cloner(client, message):
    print(f"📂 Nayi File Detect Hui: {SOURCE_CHANNEL} se...")
    for chat in DESTINATIONS:
        try:
            # Caption="" se saara text aur link hat jayega
            await message.copy(chat_id=chat, caption="") 
            print(f"✅ File copy ho gayi: {chat} mein")
        except Exception as e:
            print(f"❌ {chat} mein error: {e}")

if __name__ == "__main__":
    print("🚀 Web Server Starting...")
    Thread(target=run_web, daemon=True).start()
    print("🚀 Gourisen OSINT Mega Bot Active!")
    
    # --- RENDER EVENT LOOP FIX ---
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app.run()
