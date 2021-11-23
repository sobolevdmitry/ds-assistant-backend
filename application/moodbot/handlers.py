from assistant.settings import MOODBOT_ADMIN_ID, PYTZ_TIMEZONE
from application.moodbot.utils import extract_user_data
from application.moodbot import messages, keyboards
from application.models import Mood
from datetime import datetime
import re


def start(update, context):
    user = extract_user_data(update)
    if user['user_id'] == MOODBOT_ADMIN_ID:
        update.message.reply_text(messages.START_MESSAGE, reply_markup=keyboards.get_mood_keyboard())

def rate_mood(update, context):
    user = extract_user_data(update)
    if user['user_id'] == MOODBOT_ADMIN_ID:
        rate = int(re.search(r'\d', update.message.text).group(0))
        mood = Mood(rate=rate, created_at=datetime.now(tz=PYTZ_TIMEZONE))
        mood.save()
        update.message.reply_text(messages.RATE_MESSAGE)

def note(update, context):
    user = extract_user_data(update)
    if user['user_id'] == MOODBOT_ADMIN_ID:
        mood = Mood.objects.last()
        if mood:
            mood.description = update.message.text
            mood.save()
            update.message.reply_text(messages.NOTE_MESSAGE)
