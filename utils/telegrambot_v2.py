from django.template.defaultfilters import date as _date

from main.models import TelegramUser, Course, CourseReview

from telebot import types
import telebot, constants, datetime

bot = telebot.TeleBot(constants.TELEGRAM_BOT_TOKEN)
bot.set_webhook(url=constants.TELEGRAM_BOT_URL)


@bot.message_handler(commands=['start'])
def handle_start(message):
    register_user(message.from_user)
    course_id = extract_course_id(message.text)
    main_menu(course_id, message.from_user.id)


def leave_review(message, course_id):
    user = authorize_user(message.from_user.id)
    try:
        course = Course.objects.get(id=course_id)
    except:
        bot.send_message(user.telegram_id, 'Занятие не найдено')
        return
    CourseReview.objects.create(
        user=user,
        course=course,
        text=message.text
    )
    bot.send_message(message.from_user.id, 'Отзыв сохранен')
    main_menu(course_id, user.telegram_id)


def main_menu(course_id, user_id):
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Просмотреть отзывы')
            markup.add('Оставить отзыв')
            text = f"""Занятие: {course.name}

Выберите действие"""
            message = bot.send_message(user_id, text, reply_markup=markup)
            bot.register_next_step_handler(message, handle_review, course_id, 10)
        except:
            bot.send_message(user_id, 'Занятие не найдено')
    else:
        bot.send_message(user_id, 'Занятие не найдено')


def handle_review(message, course_id, from_=None, to_=None):
    print(message.from_user.username)
    print(course_id)
    print(from_)
    # user = authorize_user(call.data.split()[2])
    # try:
    #     course = Course.objects.get(id=course_id)
    # except:
    #     bot.send_message(user.telegram_id, 'Занятие не найдено')
    #     return
    # if message.text == 'Просмотреть отзывы':
    # elif message.text == 'Оставить отзыв':
    #     pass


def extract_course_id(text):
    if len(text.split()) > 1:
        id = text.split()[1]
        try:
            id = int(id)
        except:
            return None
        return id
    return None


def register_user(telegram_user):
    try:
        TelegramUser.objects.get(telegram_id=telegram_user.id)
    except:
        TelegramUser.objects.create(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name
        )


def authorize_user(user_id):
    try:
        user = TelegramUser.objects.get(telegram_id=user_id)
        return user
    except:
        bot.send_message(user_id, 'Занятие не найдено')


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