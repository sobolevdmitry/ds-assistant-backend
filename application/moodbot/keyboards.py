from telegram import ReplyKeyboardMarkup
from application.models import Mood
from application.moodbot import messages

def get_mood_keyboard():
    buttons = []
    for rate, mood in reversed(Mood.get_available()).items():
        buttons.append([
            messages.MOOD_TEMPLATE.format(emoji=mood['emoji'], name=mood['name'], rate=rate)
        ])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
