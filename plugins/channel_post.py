# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, LOGGER, MAX_FILE_SIZE
from helper_func import encode


@Bot.on_message(
    filters.private
    & filters.user(ADMINS)
    & ~filters.command(
        [
            "start",
            "users",
            "broadcast",
            "ping",
            "uptime",
            "batch",
            "logs",
            "genlink",
            "delvar",
            "getvar",
            "setvar",
            "speedtest",
            "update",
            "stats",
            "vars",
            "id",
            "restart",
        ]
    )
)
async def channel_post(client: Client, message: Message):
    # Check file size if it's a document
    if message.document and message.document.file_size > MAX_FILE_SIZE:
        await message.reply_text(
            f"❌ <b>File terlalu besar!</b>\n"
            f"📄 <b>
