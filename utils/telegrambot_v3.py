from __future__ import absolute_import, unicode_literals
from django.template.defaultfilters import date as _date
from uniclub_mobile.celery import app
from celery import shared_task
from main.models import TelegramUser, Course, CourseReview

from telebot import types
import telebot, constants, datetime, os

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))
bot.set_webhook(url=constants.TELEGRAM_BOT_URL)

@shared_task
def start_bot():
    bot.polling()


@bot.message_handler(commands=['start'])
def handle_start(message):
    register_user(message.from_user)
    course_id = extract_course_id(message.text)
    main_menu(course_id, message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    parameters = parse_parameters(call)
    print(parameters)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=None
    )
    if parameters[2] in [constants.TELEGRAM_ACTION_VIEW_REVIEWS,
                         constants.TELEGRAM_ACTION_LEAVE_REVIEW]:
        handle_review(parameters[0], parameters[1], parameters[2])
    elif parameters[2] == constants.TELEGRAM_ACTION_MORE_REVIEWS:
        handle_review(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])
    elif parameters[2] == constants.TELEGRAM_ACTION_BACK:
        main_menu(parameters[0], parameters[1])
    elif parameters[2] in [constants.TELEGRAM_YES, constants.TELEGRAM_NO]:
        finish_leave_review(parameters[0], parameters[1], parameters[2], parameters[3])


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, '⬆️Выберите дейсвие⬆️')

def main_menu(course_id, user_id):
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
        except:
            bot.send_message(user_id, 'Занятие не найдено')
            return
        text = f"""Занятие: {course.name}

Выберите действие"""
        message = bot.send_message(user_id, text, reply_markup=get_main_markup(course_id, user_id))
    else:
        bot.send_message(user_id, 'Занятие не найдено')


def handle_review(course_id, user_id, type, from_=None, to_=None):
        if type in [constants.TELEGRAM_ACTION_VIEW_REVIEWS, constants.TELEGRAM_ACTION_MORE_REVIEWS]:
            handle_view_reviews(course_id, user_id, type, from_, to_)
        elif type == constants.TELEGRAM_ACTION_LEAVE_REVIEW:
            message = bot.send_message(user_id, 'Напишите ваш отзыв')
            bot.clear_step_handler(message)
            bot.register_next_step_handler(message, ask_anonymous, course_id)


def handle_view_reviews(course_id, user_id, type, from_, to_):
        if type in [constants.TELEGRAM_ACTION_VIEW_REVIEWS, constants.TELEGRAM_ACTION_MORE_REVIEWS]:
            user = authorize_user(user_id)
            try:
                course = Course.objects.get(id=course_id)
            except:
                bot.send_message(user.telegram_id, 'Занятие не найдено')
                return
            from_ = from_ if from_ else 0
            to_ = to_ if to_ else constants.TELEGRAM_PAGE_NUMBER
            all_reviews = course.reviews.all()
            reviews = all_reviews[from_:to_]
            if len(reviews) > 0:
                for index, review in enumerate(reviews):
                    keyboard = None
                    if index == len(reviews) - 1:
                        keyboard = get_pagination_markup(
                            course_id,
                            user_id,
                            len(all_reviews[from_ + constants.TELEGRAM_PAGE_NUMBER:to_ + constants.TELEGRAM_PAGE_NUMBER]) > 0,
                            from_ + constants.TELEGRAM_PAGE_NUMBER,
                            to_ + constants.TELEGRAM_PAGE_NUMBER
                        )
                    bot.send_message(user.telegram_id, serialize_review(review), reply_markup=keyboard)
            else:
                bot.send_message(
                    user.telegram_id,
                    'К сожалению по данному занятию отсутвуют отзывы',
                    reply_markup=get_back_markup(course_id, user_id)
                )
        elif type == constants.TELEGRAM_ACTION_BACK:
            main_menu(course_id, user_id)


def ask_anonymous(message, course_id):
    bot.send_message(
        message.from_user.id,
        'Хотите оставить отзыв анонимно?',
        reply_markup=get_yes_no_markup(
            course_id,
            message.from_user.id,
            message.text
        )
    )


def finish_leave_review(course_id, user_id, type, text):
    user = authorize_user(user_id)
    try:
        course = Course.objects.get(id=course_id)
    except:
        bot.send_message(user.telegram_id, 'Занятие не найдено')
        return
    CourseReview.objects.create(
        user=user,
        course=course,
        text=text,
        is_anonymous=type == constants.TELEGRAM_YES
    )
    bot.send_message(user_id, 'Отзыв сохранен', reply_markup=get_back_markup(course_id, user_id))


def parse_parameters(call):
    parameters = call.data.split()
    parameters[0] = int(parameters[0])
    parameters[1] = int(parameters[1])
    if parameters[2] == constants.TELEGRAM_ACTION_MORE_REVIEWS:
        parameters[3] = int(parameters[3])
        parameters[4] = int(parameters[4])
    elif parameters[2] in [constants.TELEGRAM_YES, constants.TELEGRAM_NO]:
        parameters[3] = ' '.join(parameters[3:])
    return parameters


def get_back_markup(course_id, user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            constants.TELEGRAM_BACK,
            callback_data=f'{course_id} {user_id} {constants.TELEGRAM_ACTION_BACK}'
        )
    )
    return markup


def get_pagination_markup(course_id, user_id, with_more=False, from_=None, to_=None):
    markup = types.InlineKeyboardMarkup()
    if with_more:
        markup.add(
            types.InlineKeyboardButton(
                constants.TELEGRAM_MORE_REVIEWS,
                callback_data=f'{course_id} {user_id} {constants.TELEGRAM_ACTION_MORE_REVIEWS} {from_} {to_}'
            )
        )
    markup.add(
        types.InlineKeyboardButton(
            constants.TELEGRAM_BACK,
            callback_data=f'{course_id} {user_id} {constants.TELEGRAM_ACTION_BACK}'
        )
    )
    return markup


def get_main_markup(course_id, user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            constants.TELEGRAM_VIEW_REVIEWS,
            callback_data=f'{course_id} {user_id} {constants.TELEGRAM_ACTION_VIEW_REVIEWS}'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            constants.TELEGRAM_LEAVE_REVIEW,
            callback_data=f'{course_id} {user_id} {constants.TELEGRAM_ACTION_LEAVE_REVIEW}'
        )
    )
    return markup


def get_yes_no_markup(course_id, user_id, text):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            constants.TELEGRAM_YES,
            callback_data=f'{course_id} {user_id} {constants.TELEGRAM_YES} {text}'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            constants.TELEGRAM_NO,
            callback_data=f'{course_id} {user_id} {constants.TELEGRAM_NO} {text}'
        )
    )
    return markup


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
    if review.is_anonymous:
        return f"""{review.text}

{_date(review.created_at, "d M, Y")}"""
    if review.user.first_name and review.user.username:
        name = f'{review.user.first_name} (@{review.user.username})'
    elif review.user.first_name and review.user.last_name and review.user.username:
        name = f'{review.user.first_name} {review.user.last_name} (@{review.user.username})'
    else:
        name = f'@{review.user.username}'
    return f"""{name}

{review.text}

{_date(review.created_at, "d M, Y")}"""

# app.control.purge()
#
# i = app.control.inspect()
# jobs = i.active()
# if jobs:
#     for hostname in jobs:
#         tasks = jobs[hostname]
#         for task in tasks:
#             app.control.revoke(task['id'], terminate=True)
#
# jobs = i.reserved()
# if jobs:
#     for hostname in jobs:
#         tasks = jobs[hostname]
#         for task in tasks:
#             app.control.revoke(task['id'], terminate=True)
#
# start_bot.delay()