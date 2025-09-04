# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import base64
import re

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from config import ADMINS, FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, FORCE_SUB_GROUP


async def check_membership(client, chat_id, user_id):
    """Helper function to check if user is member of a chat"""
    try:
        member = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status in [
            ChatMemberStatus.OWNER, 
            ChatMemberStatus.ADMINISTRATOR, 
            ChatMemberStatus.MEMBER
        ]
    except UserNotParticipant:
        return False
    except Exception:
        return False


async def subschannel(filter, client, update):
    if not FORCE_SUB_CHANNEL1:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    return await check_membership(client, FORCE_SUB_CHANNEL1, user_id)


async def subschannel2(filter, client, update):
    if not FORCE_SUB_CHANNEL2:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    return await check_membership(client, FORCE_SUB_CHANNEL2, user_id)


async def subsgroup(filter, client, update):
    if not FORCE_SUB_GROUP:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    return await check_membership(client, FORCE_SUB_GROUP, user_id)


async def is_subscribed(filter, client, update):
    """Check if user is subscribed to all required channels/groups"""
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    
    # Check all required subscriptions
    checks = []
    if FORCE_SUB_CHANNEL1:
        checks.append(check_membership(client, FORCE_SUB_CHANNEL1, user_id))
    if FORCE_SUB_CHANNEL2:
        checks.append(check_membership(client, FORCE_SUB_CHANNEL2, user_id))
    if FORCE_SUB_GROUP:
        checks.append(check_membership(client, FORCE_SUB_GROUP, user_id))
    
    # If no force sub is configured, allow access
    if not checks:
        return True
        
    # All checks must pass
    results = await asyncio.gather(*checks, return_exceptions=True)
    return all(result is True for result in results)


async def encode(string):
    try:
        string_bytes = string.encode("ascii")
        base64_bytes = base64.urlsafe_b64encode(string_bytes)
        base64_string = (base64_bytes.decode("ascii")).strip("=")
        return base64_string
    except Exception:
        return None


async def decode(base64_string):
    try:
        base64_string = base64_string.strip("=")
        # Add padding if needed
        base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
        string_bytes = base64.urlsafe_b64decode(base64_bytes)
        string = string_bytes.decode("ascii")
        return string
    except Exception:
        return None


async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    chunk_size = 200
    
    while total_messages < len(message_ids):
        temp_ids = message_ids[total_messages : total_messages + chunk_size]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temp_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            try:
                msgs = await client.get_messages(
                    chat_id=client.db_channel.id, message_ids=temp_ids
                )
            except Exception:
                # Skip this chunk if it fails after retry
                total_messages += len(temp_ids)
                continue
        except Exception:
            # Skip this chunk if it fails
            total_messages += len(temp_ids)
            continue
            
        total_messages += len(temp_ids)
        messages.extend(msgs)
    return messages


async def get_message_id(client, message):
    try:
        if (
            message.forward_from_chat
            and message.forward_from_chat.id == client.db_channel.id
        ):
            return message.forward_from_message_id
        elif message.forward_from_chat or message.forward_sender_name or not message.text:
            return 0
        else:
            # Improved regex pattern
            patterns = [
                r"https://t\.me/c/(-?\d+)/(\d+)",
                r"https://t\.me/([^/]+)/(\d+)"
            ]
            
            for pattern in patterns:
                matches = re.match(pattern, message.text)
                if matches:
                    channel_identifier = matches.group(1)
                    msg_id = int(matches.group(2))
                    
                    # Handle channel ID format
                    if channel_identifier.isdigit() or channel_identifier.startswith('-'):
                        channel_id = int(channel_identifier)
                        if channel_identifier.isdigit():
                            channel_id = int(f"-100{channel_identifier}")
                        if channel_id == client.db_channel.id:
                            return msg_id
                    elif channel_identifier == client.db_channel.username:
                        return msg_id
            return 0
    except Exception:
        return 0


# Create filter instances
subsgc = filters.create(subsgroup)
subsch = filters.create(subschannel)
subsch2 = filters.create(subschannel2)
subsall = filters.create(is_subscribed)
