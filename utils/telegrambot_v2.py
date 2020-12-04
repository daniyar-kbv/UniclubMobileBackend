from __future__ import absolute_import, unicode_literals
from django.template.defaultfilters import date as _date
from uniclub_mobile.celery import app
from celery import shared_task
from main.models import TelegramUser, Course, CourseReview

from telebot import types
import telebot, constants, datetime

bot = telebot.TeleBot(constants.TELEGRAM_BOT_TOKEN)
bot.set_webhook(url=constants.TELEGRAM_BOT_URL)
# bot.delete_webhook()


# @shared_task
# def start_bot():
#     bot.polling()


@bot.message_handler(commands=['start'])
def handle_start(message):
    register_user(message.from_user)
    course_id = extract_course_id(message.text)
    main_menu(course_id, message.from_user.id)


def main_menu(course_id, user_id):
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
        except:
            bot.send_message(user_id, 'Занятие не найдено')
            return
        text = f"""Занятие: {course.name}

Выберите действие"""
        message = bot.send_message(user_id, text, reply_markup=get_main_markup())
        bot.clear_step_handler(message)
        bot.register_next_step_handler(message, handle_review, course_id)
    else:
        bot.send_message(user_id, 'Занятие не найдено')


def handle_review(message, course_id, from_=None, to_=None):
    is_valid =  validate_text(
        message,
        [
            constants.TELEGRAM_VIEW_REVIEWS,
            constants.TELEGRAM_LEAVE_REVIEW
        ]
    )
    if is_valid == True:
        if message.text in [constants.TELEGRAM_VIEW_REVIEWS, constants.TELEGRAM_MORE_REVIEWS]:
            handle_view_reviews(message, course_id, from_, to_)
        elif message.text == constants.TELEGRAM_LEAVE_REVIEW:
            message = bot.send_message(message.from_user.id, 'Напишите ваш отзыв')
            bot.clear_step_handler(message)
            bot.register_next_step_handler(message, ask_anonymous, course_id)
    elif is_valid == False:
        bot.clear_step_handler(message)
        bot.register_next_step_handler(message, handle_review, course_id)
    else:
        return


def handle_view_reviews(message, course_id, from_, to_):
    is_valid = validate_text(
        message,
        [
            constants.TELEGRAM_VIEW_REVIEWS,
            constants.TELEGRAM_MORE_REVIEWS,
            constants.TELEGRAM_BACK
        ]
    )
    if is_valid == True:
        if message.text in [constants.TELEGRAM_VIEW_REVIEWS, constants.TELEGRAM_MORE_REVIEWS]:
            user = authorize_user(message.from_user.id)
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
                        keyboard = get_pagination_markup(len(all_reviews[from_ + constants.TELEGRAM_PAGE_NUMBER:to_ + constants.TELEGRAM_PAGE_NUMBER]) > 0)
                    bot.send_message(user.telegram_id, serialize_review(review), reply_markup=keyboard)
                    bot.clear_step_handler(message)
                    bot.register_next_step_handler(
                        message,
                        handle_view_reviews,
                        course_id,
                        from_ + constants.TELEGRAM_PAGE_NUMBER,
                        to_ + constants.TELEGRAM_PAGE_NUMBER
                    )
            else:
                bot.send_message(user.telegram_id, 'К сожалению по данному занятию отсутвуют отзывы')
                main_menu(course_id, user.telegram_id)
        elif message.text == constants.TELEGRAM_BACK:
            main_menu(course_id, message.from_user.id)
    elif is_valid == False:
        bot.clear_step_handler(message)
        bot.register_next_step_handler(message, handle_view_reviews, course_id, from_, to_)
    else:
        return


def ask_anonymous(message, course_id):
    bot.send_message(message.from_user.id, 'Хотите оставить отзыв анонимно?', reply_markup=get_yes_no_markup())
    bot.clear_step_handler(message)
    bot.register_next_step_handler(message, finish_leave_review, course_id, message.text)


def finish_leave_review(message, course_id, text):
    is_valid = validate_text(message, [constants.TELEGRAM_YES, constants.TELEGRAM_NO])
    if is_valid == True:
        user = authorize_user(message.from_user.id)
        try:
            course = Course.objects.get(id=course_id)
        except:
            bot.send_message(user.telegram_id, 'Занятие не найдено')
            return
        CourseReview.objects.create(
            user=user,
            course=course,
            text=text,
            is_anonymous=message.text == constants.TELEGRAM_YES
        )
        bot.send_message(message.from_user.id, 'Отзыв сохранен')
        main_menu(course_id, user.telegram_id)
    elif is_valid == False:
        bot.clear_step_handler(message)
        bot.register_next_step_handler(message, finish_leave_review, course_id, message.text)
    else:
        return


def get_pagination_markup(with_more=False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if with_more:
        keyboard.add(constants.TELEGRAM_MORE_REVIEWS)
    keyboard.add(constants.TELEGRAM_BACK)
    return keyboard


def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(constants.TELEGRAM_VIEW_REVIEWS)
    markup.add(constants.TELEGRAM_LEAVE_REVIEW)
    return markup


def get_yes_no_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(constants.TELEGRAM_YES)
    markup.add(constants.TELEGRAM_NO)
    return markup


def validate_text(message, valid_texts):
    if '/start' in message.text:
        handle_start(message)
        return None
    elif message.text in valid_texts:
        return True
    bot.send_message(message.from_user.id, 'Неверная команда')
    return False


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

# start_bot.delay()