from django.template.defaultfilters import date as _date

from main.models import TelegramUser, Course, CourseReview

from telebot import types
import telebot, constants, datetime

bot = telebot.TeleBot(constants.TELEGRAM_BOT_TOKEN)
bot.set_webhook(url=constants.TELEGRAM_BOT_URL)


@bot.message_handler(commands=['start'])
def handle_start(message):
    print('asd')
    keyboard = types.InlineKeyboardMarkup()
    key_more = types.InlineKeyboardButton(text='Посмотреть еще', callback_data='asd')
    keyboard.add(key_more)
    bot.send_message(message.from_user.id, ')', reply_markup=keyboard)
    # course_id = extract_course_id(message.text)
    # user = authorize_user(telegram_user=message.from_user)
    # if course_id:
    #     try:
    #         course = Course.objects.get(id=course_id)
    #     except:
    #         bot.send_message(message.from_user.id, 'Занятие не найдено')
    #         return
    #     user.last_course = course
    #     user.save()
    #     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    #     markup.add('Просмотреть отзывы')
    #     markup.add('Оставить отзыв')
    #     bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=markup)
    # else:
    #     bot.send_message(message.from_user.id, 'Занятие не найдено')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user = authorize_user(message.from_user.id)
    if message.text == 'Просмотреть отзывы':
        reviews = user.last_course.reviews.all()
        for index, review in enumerate(reviews[:10]):
            if index != 9:
                bot.send_message(message.from_user.id, serialize_review(review))
            else:
                keyboard = types.InlineKeyboardMarkup()
                key_more = types.InlineKeyboardButton(text='Посмотреть еще', callback_data='yes')
                keyboard.add(key_more)
                bot.send_message(message.from_user.id, serialize_review(review), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    print(call.data)


def extract_course_id(text):
    if len(text.split()) > 1:
        id = text.split()[1]
        try:
            id = int(id)
        except:
            return None
        return id
    return None


def authorize_user(telegram_user):
    try:
        user = TelegramUser.objects.get(telegram_id=telegram_user.id)
    except:
        user = TelegramUser.objects.create(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name
        )
    return user


def serialize_review(review):
    if review.user.first_name and review.user.username:
        name = f'{review.user.first_name} (@{review.user.username})'
    elif review.user.first_name and review.user.last_name and review.user.username:
        name = f'{review.user.first_name} {review.user.last_name} (@{review.user.username})'
    else:
        name = f'@{review.user.username}'
    return f"""{name}

{review.text}

{_date(review.created_at, "d M, Y")}"""