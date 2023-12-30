
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = "" # integer value, dont use ""
    API_HASH = ""
    TOKEN = ""  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 1995154708 # If you dont know, run the bot and do /id in your private chat with it, also an integer
    
    SUPPORT_CHAT = "webnet_support_chats"  # Your own group for support, do not add the @
    START_IMG = ""
    EVENT_LOGS = ()  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit# Your own group for support, do not add the @
    JOIN_LOGGER = (
        -1001253661229
    )  # Prints any new group the bot is added to, prints just the name and ID.
 
    MONGO_DB_URI= ""
    # RECOMMENDED
    DATABASE_URL = ""  # A sql database url from elephantsql.com
    CASH_API_KEY = (
        ""  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = ""
    # Get your API key from https://timezonedb.com/api

TEMP_MAIL_KEY: ""
ARQ_API: ""

# Advanced
SW_API: ""
OPENWEATHERMAP_ID: ""
WOLFRAM_ID: ""
DEBUG_MODE: False
LOAD_MODULES: True
LOGS_CHANNEL_ID: -000000000
ALLOW_FORWARDS_COMMANDS: False


    # Optional fields
    CHATBOT_API="" # get it from @FallenChat_Bot using /token
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8
    

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
