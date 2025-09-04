# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import pyromod.listen
import sys
import asyncio

from pyrogram import Client, enums
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid, FloodWait

from config import (
    API_HASH,
    APP_ID,
    CHANNEL_ID,
    FORCE_SUB_CHANNEL1,
    FORCE_SUB_CHANNEL2,
    FORCE_SUB_GROUP,
    LOGGER,
    OWNER,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self, *args, **kwargs):
        try:
            await super().start(*args, **kwargs)
        except ApiIdInvalid:
            self.LOGGER(__name__).error("❌ API_ID dan API_HASH tidak valid!")
            self.LOGGER(__name__).info("💡 Dapatkan API credentials yang valid dari https://my.telegram.org")
            sys.exit(1)
        except ApiIdPublishedFlood:
            self.LOGGER(__name__).error("❌ API_ID sudah digunakan terlalu banyak!")
            self.LOGGER(__name__).info("💡 Coba gunakan API_ID yang berbeda")
            sys.exit(1)
        except AccessTokenInvalid:
            self.LOGGER(__name__).error("❌ BOT_TOKEN tidak valid!")
            self.LOGGER(__name__).info("💡 Dapatkan bot token yang valid dari @BotFather")
            sys.exit(1)
        except FloodWait as e:
            self.LOGGER(__name__).warning(f"⏳ Flood wait: {e.x} seconds")
            await asyncio.sleep(e.x)
            return await self.start()
        except Exception as e:
            self.LOGGER(__name__).error(f"❌ Error starting bot: {e}")
            self.LOGGER(__name__).info("🆘 Join https://t.me/SharingUserbot untuk bantuan")
            sys.exit(1)

        try:
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.LOGGER(__name__).info(f"✅ Bot berhasil dimulai!")
            self.LOGGER(__name__).info(f"┌ 🤖 Nama: {self.namebot}")
            self.LOGGER(__name__).info(f"└ 👤 Username: @{self.username}")
        except Exception as e:
            self.LOGGER(__name__).error(f"❌ Error getting bot info: {e}")
            sys.exit(1)

        # Verify Force Sub Channel 1
        if FORCE_SUB_CHANNEL1:
            try:
                info = await self.get_chat(FORCE_SUB_CHANNEL1)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL1)
                    info = await self.get_chat(FORCE_SUB_CHANNEL1)
                    link = info.invite_link
                self.invitelink = link
                self.LOGGER(__name__).info(f"✅ Force Sub Channel 1 connected!")
                self.LOGGER(__name__).info(f"┌ 📢 Title: {info.title}")
                self.LOGGER(__name__).info(f"└ 🆔 Chat ID: {info.id}")
            except Exception as e:
                self.LOGGER(__name__).error(f"❌ Error with FORCE_SUB_CHANNEL1: {e}")
                self.LOGGER(__name__).error(f"💡 Pastikan @{self.username} adalah admin di channel tersebut")
                self.LOGGER(__name__).error(f"🆔 Current FORCE_SUB_CHANNEL1: {FORCE_SUB_CHANNEL1}")
                sys.exit(1)

        # Verify Force Sub Channel 2
        if FORCE_SUB_CHANNEL2:
            try:
                info = await self.get_chat(FORCE_SUB_CHANNEL2)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    info = await self.get_chat(FORCE_SUB_CHANNEL2)
                    link = info.invite_link
                self.invitelink2 = link
                self.LOGGER(__name__).info(f"✅ Force Sub Channel 2 connected!")
                self.LOGGER(__name__).info(f"┌ 📢 Title: {info.title}")
                self.LOGGER(__name__).info(f"└ 🆔 Chat ID: {info.id}")
            except Exception as e:
                self.LOGGER(__name__).error(f"❌ Error with FORCE_SUB_CHANNEL2: {e}")
                self.LOGGER(__name__).error(f"💡 Pastikan @{self.username} adalah admin di channel tersebut")
                self.LOGGER(__name__).error(f"🆔 Current FORCE_SUB_CHANNEL2: {FORCE_SUB_CHANNEL2}")
                sys.exit(1)
                
        # Verify Force Sub Group
        if FORCE_SUB_GROUP:
            try:
                info = await self.get_chat(FORCE_SUB_GROUP)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_GROUP)
                    info = await self.get_chat(FORCE_SUB_GROUP)
                    link = info.invite_link
                self.invitelink3 = link
                self.LOGGER(__name__).info(f"✅ Force Sub Group connected!")
                self.LOGGER(__name__).info(f"┌ 👥 Title: {info.title}")
                self.LOGGER(__name__).info(f"└ 🆔 Chat ID: {info.id}")
            except Exception as e:
                self.LOGGER(__name__).error(f"❌ Error with FORCE_SUB_GROUP: {e}")
                self.LOGGER(__name__).error(f"💡 Pastikan @{self.username} adalah admin di group tersebut")
                self.LOGGER(__name__).error(f"🆔 Current FORCE_SUB_GROUP: {FORCE_SUB_GROUP}")
                sys.exit(1)

        # Verify Database Channel
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            
            # Test send message
            test = await self.send_message(
                chat_id=db_channel.id, 
                text="🔧 Bot started successfully - Database test", 
                disable_notification=True
            )
            await test.delete()
            
            self.LOGGER(__name__).info(f"✅ Database Channel connected!")
            self.LOGGER(__name__).info(f"┌ 💾 Title: {db_channel.title}")
            self.LOGGER(__name__).info(f"└ 🆔 Chat ID: {db_channel.id}")
            
        except Exception as e:
            self.LOGGER(__name__).error(f"❌ Error with Database Channel: {e}")
            self.LOGGER(__name__).error(f"💡 Pastikan @{self.username} adalah admin di channel database")
            self.LOGGER(__name__).error(f"🆔 Current CHANNEL_ID: {CHANNEL_ID}")
            self.LOGGER(__name__).info("🆘 Join https://t.me/SharingUserbot untuk bantuan")
            sys.exit(1)

        # Set parse mode
        self.set_parse_mode(enums.ParseMode.HTML)
        
        # Success message
        self.LOGGER(__name__).info("🎉" + "="*50)
        self.LOGGER(__name__).info("🔥 BOT BERHASIL DIAKTIFKAN! 🔥")
        self.LOGGER(__name__).info("="*52)
        self.LOGGER(__name__).info(f"👨‍💻 Bot Owner: @{OWNER}")
        self.LOGGER(__name__).info("🆘 Support: https://t.me/SharingUserbot") 
        self.LOGGER(__name__).info("📖 Source: https://github.com/mrismanaziz/File-Sharing-Man")
        self.LOGGER(__name__).info("="*52)

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("🛑 Bot stopped.")
