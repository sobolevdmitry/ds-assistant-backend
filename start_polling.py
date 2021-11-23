import os
import django

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assistant.settings')
    django.setup()
    from application.moodbot.dispatcher import start_polling
    start_polling()


if __name__ == "__main__":
    main()
