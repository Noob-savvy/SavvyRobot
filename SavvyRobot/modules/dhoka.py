#khud banaya hai kang karna hai toh credit de dena
import html
import random
import time

from typing import Optional
from telegram import ParseMode, Update, ChatPermissions
from telegram.ext import CallbackContext, run_async
from tswift import Song
from telegram.error import BadRequest

import SavvyRobot.modules.dhoka_strings as dhoka_strings
from SavvyRobot import dispatcher
from SavvyRobot.modules.disable import DisableAbleCommandHandler
from SavvyRobot.modules.helper_funcs.alternate import send_message, typing_action
from SavvyRobot.modules.helper_funcs.chat_status import (is_user_admin)
from SavvyRobot.modules.helper_funcs.extraction import extract_user

@run_async
def dhoka(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(dhoka_strings.DHOKA))



DHOKA_HANDLER = DisableAbleCommandHandler("dhoka", dhoka)

dispatcher.add_handler(DHOKA_HANDLER)
