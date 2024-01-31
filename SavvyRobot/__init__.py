# <============================================== IMPORTS =========================================================>
import asyncio
import json
import logging
import os
import sys
import time
from random import choice

import telegram
import telegram.ext as tg
from pyrogram import Client, errors
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, ApplicationBuilder
from telethon import TelegramClient, events
from telethon.sessions import MemorySession

# <=======================================================================================================>
StartTime = time.time()

loop = asyncio.get_event_loop()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:

    API_ID = int(os.environ.get("API_ID", None))
    API_HASH = os.environ.get("API_HASH", None)
    
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    DB_URI = os.environ.get("DATABASE_URL")
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    INFOPIC = bool(os.environ.get("INFOPIC", "True"))
    LOAD = os.environ.get("LOAD", "").split()
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    START_IMG = os.environ.get(
        "START_IMG", ""
    )
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "THE_WEBNET_NETWORK")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    TOKEN = os.environ.get("TOKEN", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    WORKERS = int(os.environ.get("WORKERS", 8))

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "6688753848").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

else:
    from SavvyRobot.config import Development as Config

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ALLOW_CHATS = Config.ALLOW_CHATS
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    DB_URI = Config.DATABASE_URL
    DEL_CMDS = Config.DEL_CMDS
    EVENT_LOGS = Config.EVENT_LOGS
    INFOPIC = Config.INFOPIC
    LOAD = Config.LOAD
    MONGO_DB_URI = Config.MONGO_DB_URI
    NO_LOAD = Config.NO_LOAD
    START_IMG = Config.START_IMG
    STRICT_GBAN = Config.STRICT_GBAN
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    TOKEN = Config.TOKEN
    TIME_API_KEY = Config.TIME_API_KEY
    WORKERS = Config.WORKERS

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in Config.DEMONS or [])
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in Config.TIGERS or [])
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in Config.WOLVES or [])
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")


DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(6755880898)

# <============================================== INITIALIZE APPLICATION =========================================================>
# Initialize the application builder and add a handler
dispatcher = Application.builder().token(TOKEN).build()
function = dispatcher.add_handler
# <=======================================================================================================>

# <================================================ BOOT MESSAGE=======================================================>
ALIVE_MSG = """
💫 *MY SYSTEM IS STARTING, PLEASE WAIT FOR SOMETIME TO COMPLETE BOOT!*


*IF COMMANDS DON'T WORK CHECK THE LOGS*
"""

ALIVE_IMG = [
    "https://telegra.ph/file/40b93b46642124605e678.jpg",
    "https://telegra.ph/file/01a2e0cd1b9d03808c546.jpg",
    "https://telegra.ph/file/ed4385c26dcf6de70543f.jpg",
    "https://telegra.ph/file/33a8d97739a2a4f81ddde.jpg",
    "https://telegra.ph/file/cce9038f6a9b88eb409b5.jpg",
    "https://telegra.ph/file/262c86393730a609cdade.jpg",
    "https://telegra.ph/file/33a8d97739a2a4f81ddde.jpg",
]
# <=======================================================================================================>


# <==================================================== BOOT FUNCTION ===================================================>
async def send_booting_message():
    bot = dispatcher.bot

    try:
        await bot.send_photo(
            chat_id=SUPPORT_ID,
            photo=str(choice(ALIVE_IMG)),
            caption=ALIVE_MSG,
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        LOGGER.warning(
            "[ERROR] - Bot isn't able to send a message to the support_chat!"
        )
        print(e)


# <=======================================================================================================>


# <================================================= EXTBOT ======================================================>
loop.run_until_complete(
    asyncio.gather(dispatcher.bot.initialize(), send_booting_message())
)
# <=======================================================================================================>

# <=============================================== CLIENT SETUP ========================================================>
# Create the Mikobot and TelegramClient instances
pbot = Client("SavvyRobot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
# <=======================================================================================================>

# <=============================================== GETTING BOT INFO ========================================================>
# Get bot information
print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username
# <=======================================================================================================>

# <================================================== CONVERT LISTS =====================================================>
# Convert sets to lists for further use
SUPPORT_STAFF = (
    [int(OWNER_ID)] + list(DRAGONS) + list(WOLVES) + list(DEMONS) + list(DEV_USERS)
)
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)
# <====================================================  ===================================================>

# Load at end to ensure all prev variables have been set
from SavvyRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
