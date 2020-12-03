import telebot, constants

bot = telebot.TeleBot(constants.TELEGRAM_BOT_TOKEN)
bot.set_webhook(url=constants.TELEGRAM_BOT_URL)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    print(message.text)
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))
