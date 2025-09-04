# Credits: @mrismanaziz
# FROM File-Sharing-Man <https://github.com/mrismanaziz/File-Sharing-Man/>
# t.me/SharingUserbot & t.me/Lunatic0de

from config import FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, FORCE_SUB_GROUP
from pyrogram.types import InlineKeyboardButton


def start_button(client):
    """Generate start buttons based on force sub configuration"""
    buttons = []
    
    # Add force sub buttons if configured
    fsub_buttons = []
    if FORCE_SUB_CHANNEL1:
        fsub_buttons.append(InlineKeyboardButton(text="📢 Channel 1", url=client.invitelink))
    if FORCE_SUB_CHANNEL2:
        fsub_buttons.append(InlineKeyboardButton(text="📢 Channel 2", url=client.invitelink2))
    if FORCE_SUB_GROUP:
        fsub_buttons.append(InlineKeyboardButton(text="👥 Group", url=client.invitelink3))
    
    # Add fsub buttons in rows of 2
    for i in range(0, len(fsub_buttons), 2):
        buttons.append(fsub_buttons[i:i+2])
    
    # Add help and close buttons
    buttons.append([
        InlineKeyboardButton(text="❓ Help & Commands", callback_data="help"),
        InlineKeyboardButton(text="❌ Close", callback_data="close"),
    ])
    
    return buttons


def fsub_button(client, message):
    """Generate force subscribe buttons"""
    buttons = []
    
    # Add subscription buttons
    fsub_row = []
    if FORCE_SUB_CHANNEL1:
        fsub_row.append(InlineKeyboardButton(text="📢 CH 1", url=client.invitelink))
    if FORCE_SUB_CHANNEL2:
        fsub_row.append(InlineKeyboardButton(text="📢 CH 2", url=client.invitelink2))
    if FORCE_SUB_GROUP:
        fsub_row.append(InlineKeyboardButton(text="👥 Group", url=client.invitelink3))
    
    # Split into multiple rows if too many buttons
    for i in range(0, len(fsub_row), 2):
        buttons.append(fsub_row[i:i+2])
    
    # Add try again button
    try:
        if len(message.command) > 1:
            buttons.append([
                InlineKeyboardButton(
                    text="🔄 Coba Lagi",
                    url=f"https://t.me/{client.username}?start={message.command[1]}",
                )
            ])
    except (IndexError, AttributeError):
        pass
    
    return buttons
