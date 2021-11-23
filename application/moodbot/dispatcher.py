from telegram.ext import (
    Dispatcher, Updater, Defaults,
    CommandHandler, MessageHandler, Filters
)
from assistant.settings import MOODBOT_TOKEN, MOODBOT_DEFAULTS
from application.moodbot.bot import bot
from application.moodbot import handlers, messages
from application.models import Mood
import re
import logging

logger = logging.getLogger(__name__)

def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", handlers.start))
    for rate, mood in Mood.get_available().items():
        dp.add_handler(MessageHandler(
            Filters.text &
            Filters.regex(re.escape(messages.MOOD_TEMPLATE.format(emoji=mood['emoji'], name=mood['name'], rate=rate))), handlers.rate_mood))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handlers.note))
    return dp


def start_polling():
    updater = Updater(MOODBOT_TOKEN, defaults=Defaults(**MOODBOT_DEFAULTS))
    updater.dispatcher = setup_dispatcher(updater.dispatcher)
    updater.start_polling()
    updater.idle()


dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=0, use_context=True))
