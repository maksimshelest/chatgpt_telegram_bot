import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def start(update, context):
    update.message.reply_text('Привіт! Я бот з ChatGPT. Запитай мене щось.')

def help_command(update, context):
    update.message.reply_text('Просто напиши мені повідомлення, і я спробую відповісти.')

def handle_message(update, context):
    user_message = update.message.text
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=user_message,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        bot_response = response.choices[0].text.strip()
        update.message.reply_text(bot_response)
    except Exception as e:
        print(f"Помилка OpenAI: {e}")
        update.message.reply_text('Вибачте, сталася помилка при обробці запиту.')

def error(update, context):
    print(f'Update {update} викликав помилку {context.error}')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
