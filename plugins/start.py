# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
from datetime import datetime
from time import time

from bot import Bot
from config import (
    ADMINS,
    CUSTOM_CAPTION,
    DISABLE_CHANNEL_BUTTON,
    FORCE_MSG,
    MAX_FILE_SIZE,
    MESSAGE_DELAY,
    PROTECT_CONTENT,
    START_MSG,
)
from database.sql import add_user, delete_user, full_userbase, query_msg
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from pyrogram.types import InlineKeyboardMarkup, Message

from helper_func import decode, get_messages, subsall, subsch, subsgc, subsch2

from .button import fsub_button, start_button

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60**2 * 24),
    ("hour", 60**2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)


@Bot.on_message(filters.command("start") & filters.private & subsall & subsch & subsgc & subsch2)
async def start_command(client: Bot, message: Message):
    id = message.from_user.id
    user_name = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else message.from_user.first_name
    )

    try:
        await add_user(id, user_name)
    except Exception:
        pass
        
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except Exception:
            return
            
        string = await decode(base64_string)
        if not string:
            await message.reply_text("❌ <b>Link tidak valid!</b>")
            return
            
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except Exception:
                await message.reply_text("❌ <b>Link tidak valid!</b>")
                return
                
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
                        
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception:
                await message.reply_text("❌ <b>Link tidak valid!</b>")
                return
        else:
            await message.reply_text("❌ <b>Link tidak valid!</b>")
            return
            
        temp_msg = await message.reply("<code>Tunggu Sebentar...</code>")
        
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await temp_msg.edit_text("❌ <b>Terjadi kesalahan saat mengambil file!</b>")
            return
            
        await temp_msg.delete()

        if not messages:
            await message.reply_text("❌ <b>File tidak ditemukan!</b>")
            return

        sent_count = 0
        for msg in messages:
            if not msg:  # Skip None messages
                continue
                
            # Check file size limit
            if msg.document and msg.document.file_size > MAX_FILE_SIZE:
                await message.reply_text(
                    f"❌ <b>File {msg.document.file_name} terlalu besar! "
                    f"Maksimal {MAX_FILE_SIZE / 1024 / 1024:.1f} MB</b>"
                )
                continue

            try:
                if bool(CUSTOM_CAPTION) and bool(msg.document):
                    caption = CUSTOM_CAPTION.format(
                        previouscaption=msg.caption.html if msg.caption else "",
                        filename=msg.document.file_name,
                    )
                else:
                    caption = msg.caption.html if msg.caption else ""

                reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None
                
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    protect_content=PROTECT_CONTENT,
                    reply_markup=reply_markup,
                )
                sent_count += 1
                await asyncio.sleep(MESSAGE_DELAY)
                
            except FloodWait as e:
                await asyncio.sleep(e.x)
                try:
                    await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        protect_content=PROTECT_CONTENT,
                        reply_markup=reply_markup,
                    )
                    sent_count += 1
                except Exception:
                    pass
            except Exception:
                pass
                
        if sent_count == 0:
            await message.reply_text("❌ <b>Tidak ada file yang berhasil dikirim!</b>")
        elif sent_count < len([m for m in messages if m]):
            await message.reply_text(
                f"⚠️ <b>Berhasil mengirim {sent_count} dari {len([m for m in messages if m])} file</b>"
            )
    else:
        out = start_button(client)
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name or "",
                username=f"@{message.from_user.username}"
                if message.from_user.username
                else "Tidak ada username",
                mention=message.from_user.mention,
                id=message.from_user.id,
            ),
            reply_markup=InlineKeyboardMarkup(out),
            disable_web_page_preview=True,
            quote=True,
        )


@Bot.on_message(filters.command("start") & filters.private)
async def not_joined(client: Bot, message: Message):
    buttons = fsub_button(client, message)
    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name or "",
            username=f"@{message.from_user.username}"
            if message.from_user.username
            else "Tidak ada username",
            mention=message.from_user.mention,
            id=message.from_user.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True,
    )


@Bot.on_message(filters.command(["users", "stats"]) & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(
        chat_id=message.chat.id, text="<code>Processing ...</code>"
    )
    try:
        users = await full_userbase()
        await msg.edit(f"📊 <b>{len(users)} pengguna terdaftar menggunakan bot ini</b>")
    except Exception as e:
        await msg.edit(f"❌ <b>Error: {str(e)}</b>")


@Bot.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if not message.reply_to_message:
        await message.reply_text(
            "❌ <b>Gunakan perintah ini dengan reply ke pesan yang ingin di-broadcast!</b>"
        )
        return
        
    query = await query_msg()
    broadcast_msg = message.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    pls_wait = await message.reply(
        "<code>Broadcasting Message... Tunggu Sebentar...</code>"
    )
    
    for row in query:
        chat_id = int(row[0])
        if chat_id not in ADMINS:
            try:
                await broadcast_msg.copy(chat_id, protect_content=PROTECT_CONTENT)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                try:
                    await broadcast_msg.copy(chat_id, protect_content=PROTECT_CONTENT)
                    successful += 1
                except Exception:
                    unsuccessful += 1
            except UserIsBlocked:
                await delete_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await delete_user(chat_id)
                deleted += 1
            except Exception:
                unsuccessful += 1
            total += 1
            
            # Progress update every 50 users
            if total % 50 == 0:
                try:
                    await pls_wait.edit(
                        f"<code>Broadcasting... {total} users processed</code>"
                    )
                except Exception:
                    pass
                    
    status = f"""✅ <b>Broadcast Selesai!</b>

📊 <b>Statistik:</b>
• <b>Total Pengguna:</b> <code>{total}</code>
• <b>Berhasil:</b> <code>{successful}</code>
• <b>Gagal:</b> <code>{unsuccessful}</code>
• <b>Pengguna Diblokir:</b> <code>{blocked}</code>
• <b>Akun Terhapus:</b> <code>{deleted}</code>"""
    
    await pls_wait.edit(status)


@Bot.on_message(filters.command("ping"))
async def ping_pong(client, m: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    m_reply = await m.reply_text("🏓 Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🏓 <b>PONG!!</b>\n"
        f"📶 <b>Ping:</b> <code>{delta_ping * 1000:.3f}ms</code>\n"
        f"⏰ <b>Uptime:</b> <code>{uptime}</code>"
    )


@Bot.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 <b>Status Bot:</b>\n"
        f"⏰ <b>Uptime:</b> <code>{uptime}</code>\n"
        f"🕐 <b>Start Time:</b> <code>{START_TIME_ISO}</code>"
    )
