#myapp/telegrambot.py
# Example code for telegrambot.py module
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    print(error)


def main():
    dp = DjangoTelegramBot.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler([Filters.text], echo))

    dp.add_error_handler(error)
