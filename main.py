import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from pyrogram.errors import UserNotParticipant

# --- RENDER PORT BINDING (Flask) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Gourisen OSINT Bot is Live! 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# --- CONFIGURATION (Aapka Pura Data) ---
API_ID = 37314366
API_HASH = "bd4c934697e7e91942ac911a5a287b46"
STRING_SESSION = "AQI5Xz4ASE6O7locP7_vLrorMTsXT3u80PL1M3tt20Ty8FavBKQdfbZOWjQFyai9DI46XwNhspJZO7S-V7X9JigDkGjAIfF9swyWqmvkRm1uxxR3ajE9rc4IueYDhBY60CeGk_S0FdD9IAQDmjiycLIOAI4PEvKrP5wi-5i6ecZCz4gxbpmyX5o-S8JnVfv51kivPaXVN3ioFP_TB01cgH29aJ9Oa7axnPKlTaq7hadmFfVEttBthtiT2rLz9QkX9CYmEaCJHopr8W1NqR9Is9VOPo6Y2HUGu_kh8mT1y3mgUswR_942rVYYvX43HQuq2wh1zvkf70PbVl89-2DTVHsKLrv9qQAAAAHxiovLAA"

# Force Join Settings
FORCE_CHANNELS = [-1003387459132, -1003892920891, -1003851555909, -1003601267291]
OTP_GC_LINK = "https://t.me/otpMgroup"

# OTP Settings
OTP_SOURCE = -1003087662000
OTP_DEST = "otpMgroup"
TARGET_BOTS = ["junaidaliRebot", "JunaidnnRebot"]

# File Cloner Settings
SOURCE_CHANNEL = "Junaidniz" 
DESTINATIONS = ["otpMgroup", -1003387459132, -1003892920891, -1003851555909, -1003601267291] 

app = Client("GourisenMegaBot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# --- LOGIC: FORCE JOIN CHECKER ---
async def check_sub(user_id):
    for cid in FORCE_CHANNELS:
        try:
            await app.get_chat_member(cid, user_id)
        except UserNotParticipant:
            return False
        except:
            continue
    return True

# --- FEATURE 1: START COMMAND WITH BUTTONS ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    if await check_sub(message.from_user.id):
        await message.reply_text(
            "✅ <b>Aapne saare channels join kar liye hain!</b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Go to OTP Group 🚀", url=OTP_GC_LINK)]]),
            parse_mode=ParseMode.HTML
        )
    else:
        buttons = [[InlineKeyboardButton(f"Join Channel {i+1} 📢", url=f"https://t.me/c/{str(cid)[4:]}/1")] for i, cid in enumerate(FORCE_CHANNELS)]
        buttons.append([InlineKeyboardButton("Done / Check Again ✅", callback_data="recheck")])
        await message.reply_text("🚀 <b>Gourisen OSINT Bot</b>\n\nAage badhne ke liye saare channels join karein!", reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)

@app.on_callback_query(filters.regex("recheck"))
async def recheck_cb(client, cb):
    if await check_sub(cb.from_user.id):
        await cb.message.edit_text("✅ <b>Verified!</b> Niche button click karein.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Go to OTP Group 🚀", url=OTP_GC_LINK)]]), parse_mode=ParseMode.HTML)
    else:
        await cb.answer("❌ Abhi bhi kuch channels baki hain!", show_alert=True)

# --- FEATURE 2: OTP FORWARDER ---
@app.on_message(filters.chat(OTP_SOURCE))
async def otp_logic(client, message):
    sender = message.from_user.username if message.from_user else ""
    if sender in TARGET_BOTS:
        text = message.text or message.caption
        if text:
            # Credit hatana & Quote style
            clean = text.split("Powered By")[0].strip() if "Powered By" in text else text.strip()
            final = f"<blockquote>{clean}</blockquote>\n⚡ Powered by @MAGMAxRICH"
            await client.send_message(OTP_DEST, final, parse_mode=ParseMode.HTML)

# --- FEATURE 3: FILE CLONER ---
@app.on_message(filters.chat(SOURCE_CHANNEL) & (filters.document | filters.video | filters.photo | filters.audio))
async def file_cloner(client, message):
    for dest in DESTINATIONS:
        try:
            await message.copy(dest, caption="") 
        except:
            pass

# --- RENDER RUNNER ---
async def start_bot():
    threading.Thread(target=run_flask, daemon=True).start()
    await app.start()
    print("🚀 Bot is Online!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())