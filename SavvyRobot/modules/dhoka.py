# khud banaya hai kang karna hai toh credit de dena
import random

from telegram import Update
from telegram.ext import CallbackContext, run_async

import SavvyRobot.modules.dhoka_strings as dhoka_strings
from SavvyRobot import dispatcher
from SavvyRobot.modules.disable import DisableAbleCommandHandler


@run_async
def dhoka(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(dhoka_strings.DHOKA))


DHOKA_HANDLER = DisableAbleCommandHandler("dhoka", dhoka)

dispatcher.add_handler(DHOKA_HANDLER)
