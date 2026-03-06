import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.enums import ParseMode

# --- RENDER PORT BINDING (Bas Render ko Live rakhne ke liye) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Gourisen OSINT Mega Bot is Live! 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

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

# --- FEATURE 1: OTP FORWARDER (Wahi Purana System) ---
@app.on_message(filters.chat(OTP_SOURCE))
async def otp_logic(client, message):
    sender = message.from_user.username if message.from_user else ""
    if sender in TARGET_BOTS:
        text = message.text or message.caption
        if text:
            # Credit hatana
            clean_text = text.split("Powered By")[0].strip() if "Powered By" in text else text.strip()
            # Quote + Branding
            final_msg = f"<blockquote>{clean_text}</blockquote>\n⚡ Powered by @MAGMAxRICH"
            
            await client.send_message(
                chat_id=OTP_DEST, 
                text=final_msg,
                parse_mode=ParseMode.HTML
            )
            print(f"✅ OTP Bhej Diya!")

# --- FEATURE 2: FILE CLONER (Sirf File, No Text) ---
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

# --- PYTHON 3.14 RENDER FIX ---
async def main():
    threading.Thread(target=run_flask, daemon=True).start()
    await app.start()
    print("🚀 Gourisen OSINT Mega Bot Active!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
