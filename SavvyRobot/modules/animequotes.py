# Made By @Madepranav On Telegram & Github Id Superboyfan
import random

from telegram import Update
from telegram.ext import CallbackContext, run_async

import SavvyRobot.modules.animequotesstring as animequotesstring
from SavvyRobot import dispatcher
from SavvyRobot.modules.disable import DisableAbleCommandHandler


@run_async
def animequotes(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(animequotesstring.ANIMEQUOTES))


ANIMEQUOTES_HANDLER = DisableAbleCommandHandler("animequotes", animequotes)

dispatcher.add_handler(ANIMEQUOTES_HANDLER)
