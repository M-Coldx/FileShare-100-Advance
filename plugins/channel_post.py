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
            f"📄 <b>Nama File:</b> <code>{message.document.file_name}</code>\n"
            f"📊 <b>Ukuran File:</b> <code>{message.document.file_size / 1024 / 1024:.2f} MB</code>\n"
            f"⚠️ <b>Maksimal:</b> <code>{MAX_FILE_SIZE / 1024 / 1024:.1f} MB</code>",
            quote=True
        )
        return

    reply_text = await message.reply_text("<code>📤 Mengunggah ke database...</code>", quote=True)
    
    try:
        post_message = await message.copy(
            chat_id=client.db_channel.id, disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        try:
            post_message = await message.copy(
                chat_id=client.db_channel.id, disable_notification=True
            )
        except Exception as e:
            LOGGER(__name__).error(f"Failed to copy message after flood wait: {e}")
            await reply_text.edit_text("❌ <b>Gagal mengunggah file setelah menunggu!</b>")
            return
    except Exception as e:
        LOGGER(__name__).error(f"Failed to copy message: {e}")
        await reply_text.edit_text("❌ <b>Gagal mengunggah file ke database!</b>")
        return
        
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    
    if not base64_string:
        await reply_text.edit_text("❌ <b>Gagal membuat link!</b>")
        return
        
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Share Link", url=f"https://telegram.me/share/url?url={link}")],
        [InlineKeyboardButton("📋 Copy Link", callback_data=f"copy_{base64_string}")]
    ])

    file_info = ""
    if message.document:
        file_info = f"\n📄 <b>File:</b> <code>{message.document.file_name}</code>\n📊 <b>Size:</b> <code>{message.document.file_size / 1024 / 1024:.2f} MB</code>"
    elif message.photo:
        file_info = "\n🖼 <b>Type:</b> Photo"
    elif message.video:
        file_info = f"\n🎥 <b>Type:</b> Video\n⏱ <b>Duration:</b> <code>{message.video.duration}s</code>"

    await reply_text.edit(
        f"✅ <b>Link berhasil dibuat!</b>{file_info}\n\n🔗 <b>Link:</b>\n<code>{link}</code>",
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(
                InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔗 Share Link", url=f"https://telegram.me/share/url?url={link}")]
                ])
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            try:
                await post_message.edit_reply_markup(
                    InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔗 Share Link", url=f"https://telegram.me/share/url?url={link}")]
                    ])
                )
            except Exception:
                pass
        except Exception:
            pass


@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    
    if not base64_string:
        return
        
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Share Link", url=f"https://telegram.me/share/url?url={link}")]
    ])
    
    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        try:
            await message.edit_reply_markup(reply_markup)
        except Exception:
            pass
    except Exception:
        pass


# Callback handler for copy link button
@Bot.on_callback_query(filters.regex(r"^copy_"))
async def copy_link_callback(client: Client, callback_query):
    try:
        base64_string = callback_query.data.split("_", 1)[1]
        link = f"https://t.me/{client.username}?start={base64_string}"
        await callback_query.answer(
            f"Link copied: {link}",
            show_alert=True
        )
    except Exception:
        await callback_query.answer("❌ Error copying link!", show_alert=True)
