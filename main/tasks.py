from django.contrib.auth.models import User
from celery import shared_task

from main.models import Course

import telebot, constants


# @shared_task
# def bot():
#     bot = telebot.TeleBot(constants.TELEGRAM_BOT_TOKEN)
#
#     keyboard1 = telebot.types.ReplyKeyboardMarkup()
#     keyboard1.row('Список клубов', 'Найти клуб по id')
#
#     @bot.message_handler(commands=['start'])
#     def start_message(message):
#         bot.send_message(message.chat.id, 'Привет', reply_markup=keyboard1)
#
#     @bot.message_handler(content_types=['text'])
#     def send_text(message):
#         if message.text.lower() == 'список клубов':
#             for course in Course.objects.all():
#                 keyboard = telebot.types.InlineKeyboardMarkup()
#                 callback_data = {
#                     'id': course.id
#                 }
#                 key_yes = telebot.types.InlineKeyboardButton(text='Посмотреть отзывы', callback_data=callback_data)
#                 keyboard.add(key_yes)
#                 text = f"""{course.name}
#                 """
#                 bot.send_message(message.chat.id, text, reply_markup=keyboard)
#         elif message.text.lower() == 'найти клуб по id':
#             bot.send_message(message.chat.id, 'Прощай, создатель')
#
#     bot.polling()
