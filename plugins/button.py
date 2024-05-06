# Credits: @mrismanaziz
# FROM File-Sharing-Man <https://github.com/mrismanaziz/File-Sharing-Man/>
# t.me/SharingUserbot & t.me/Lunatic0de

from config import FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, FORCE_SUB_GROUP
from pyrogram.types import InlineKeyboardButton


def start_button(client):
    if not FORCE_SUB_CHANNEL1 and not FORCE_SUB_CHANNEL2 and not FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help"),
                InlineKeyboardButton(text="ᴛᴜᴛᴜᴘ", callback_data="close"),
            ],
        ]
        return buttons
    if FORCE_SUB_CHANNEL1 and not FORCE_SUB_CHANNEL2 and not FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ 1", url=client.invitelink),
            ],
            [
                InlineKeyboardButton(text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help"),
                InlineKeyboardButton(text="ᴛᴜᴛᴜᴘ", callback_data="close"),
            ],
        ]
        return buttons
    if not FORCE_SUB_CHANNEL1 and FORCE_SUB_CHANNEL2 and not FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ 2", url=client.invitelink2),
            ],
            [
                InlineKeyboardButton(text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help"),
                InlineKeyboardButton(text="ᴛᴜᴛᴜᴘ", callback_data="close"),
            ],
        ]
        return buttons
    if not FORCE_SUB_CHANNEL1 and not FORCE_SUB_CHANNEL2 and FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ɢʀᴏᴜᴘ", url=client.invitelink3),
            ],
            [
                InlineKeyboardButton(text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help"),
                InlineKeyboardButton(text="ᴛᴜᴛᴜᴘ", callback_data="close"),
            ],
        ]
        return buttons
    if FORCE_SUB_CHANNEL1 and FORCE_SUB_CHANNEL2 and FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help"),
            ],
            [
                InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ 1", url=client.invitelink),
                InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ 2", url=client.invitelink2),
                InlineKeyboardButton(text="ɢʀᴏᴜᴘ", url=client.invitelink3),
            ],
            [InlineKeyboardButton(text="ᴛᴜᴛᴜᴘ", callback_data="close")],
        ]
        return buttons


def fsub_button(client, message):
    if FORCE_SUB_CHANNEL1 and not FORCE_SUB_CHANNEL2 and not FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ᴄʜ ɪɴᴠ", url=client.invitelink),
            ],
        ]
        try:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="ᴄᴏʙᴀ ʟᴀɢɪ",
                        url=f"https://t.me/{client.username}?start={message.command[1]}",
                    )
                ]
            )
        except IndexError:
            pass
        return buttons
    if not FORCE_SUB_CHANNEL1 and FORCE_SUB_CHANNEL2 and not FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ᴄʜ sᴄʀ", url=client.invitelink2),
            ],
        ]
        try:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="ᴄᴏʙᴀ ʟᴀɢɪ",
                        url=f"https://t.me/{client.username}?start={message.command[1]}",
                    )
                ]
            )
        except IndexError:
            pass
        return buttons
    if not FORCE_SUB_CHANNEL1 and not FORCE_SUB_CHANNEL2 and FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ɢᴄ ʙʟʜ", url=client.invitelink3),
            ],
        ]
        try:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="ᴄᴏʙᴀ ʟᴀɢɪ",
                        url=f"https://t.me/{client.username}?start={message.command[1]}",
                    )
                ]
            )
        except IndexError:
            pass
        return buttons
    if FORCE_SUB_CHANNEL1 and FORCE_SUB_CHANNEL2 and FORCE_SUB_GROUP:
        buttons = [
            [
                InlineKeyboardButton(text="ᴄʜ ɪɴᴠ", url=client.invitelink),
                InlineKeyboardButton(text="ᴄʜ sᴄʀ", url=client.invitelink2),
                InlineKeyboardButton(text="ɢᴄ ʙʟʜ", url=client.invitelink3),
            ],
        ]
        try:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="ᴄᴏʙᴀ ʟᴀɢɪ",
                        url=f"https://t.me/{client.username}?start={message.command[1]}",
                    )
                ]
            )
        except IndexError:
            pass
        return buttons
