from telegram import Bot
from telegram.ext import Defaults
from assistant.settings import MOODBOT_TOKEN, MOODBOT_DEFAULTS

bot = Bot(MOODBOT_TOKEN, defaults=Defaults(**MOODBOT_DEFAULTS))
