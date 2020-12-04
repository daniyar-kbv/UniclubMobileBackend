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


def main_menu(course_id, user_id):
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
        except:
            bot.send_message(user_id, 'Занятие не найдено')
            return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(constants.TELEGRAM_VIEW_REVIEWS)
        markup.add(constants.TELEGRAM_LEAVE_REVIEW)
        text = f"""Занятие: {course.name}

Выберите действие"""
        message = bot.send_message(user_id, text, reply_markup=markup)
        bot.register_next_step_handler(message, handle_review, course_id)
    else:
        bot.send_message(user_id, 'Занятие не найдено')


def handle_review(message, course_id, from_=None, to_=None):
    user = authorize_user(message.from_user.id)
    if validate_text(
            message.text,
            [
                constants.TELEGRAM_VIEW_REVIEWS,
                constants.TELEGRAM_LEAVE_REVIEW,
                constants.TELEGRAM_MORE_REVIEWS,
                constants.TELEGRAM_BACK
            ]
    ):
        if message.text in [constants.TELEGRAM_VIEW_REVIEWS, constants.TELEGRAM_MORE_REVIEWS]:
            hanle_view_reviews(message, course_id, user, from_, to_)
        elif message.text == constants.TELEGRAM_LEAVE_REVIEW:
            message = bot.send_message(user.telegram_id, 'Напишите ваш отзыв')
            bot.register_next_step_handler(message, ask_anonymous, course_id)
        elif message.text == constants.TELEGRAM_BACK:
            main_menu(course_id, user.telegram_id)
    else:
        handle_review(message, course_id, from_, to_)


def hanle_view_reviews(message, course_id, user, from_, to_):
    print('1')
    try:
        course = Course.objects.get(id=course_id)
    except:
        bot.send_message(user.telegram_id, 'Занятие не найдено')
        return
    print('2')
    from_ = from_ if from_ else 0
    to_ = to_ if to_ else 10
    reviews = course.reviews.all()[from_:to_]
    if reviews.count() > 0:
        for index, review in enumerate(reviews):
            keyboard = None
            if index == reviews.count() - 1:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if reviews[from_ + constants.TELEGRAM_PAGE_NUMBER:to_ + constants.TELEGRAM_PAGE_NUMBER].count > 0:
                    keyboard.add(constants.TELEGRAM_MORE_REVIEWS)
                keyboard.add(constants.TELEGRAM_BACK)
            bot.send_message(user.telegram_id, serialize_review(review), reply_markup=keyboard)
            bot.register_next_step_handler(
                message,
                handle_review,
                course_id,
                from_ + constants.TELEGRAM_PAGE_NUMBER,
                to_ + constants.TELEGRAM_PAGE_NUMBER
            )
    else:
        bot.send_message(user.telegram_id, 'К сожалению по данному занятию отсутвуют отзывы')
        main_menu(course_id, user.telegram_id)


def ask_anonymous(message, course_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(constants.TELEGRAM_YES)
    markup.add(constants.TELEGRAM_NO)
    bot.send_message('Хотите оставить отзыв анонимно?', reply_markup=markup)
    bot.register_next_step_handler(message, finish_leave_review, course_id, message.text)


def finish_leave_review(message, course_id, text):
    if validate_text(message.text, [constants.TELEGRAM_YES, constants.TELEGRAM_NO]):
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
    else:
        finish_leave_review(message, course_id, text)


def validate_text(text, valid_texts):
    if text in valid_texts:
        return True
    bot.send_message('Неверная команда')
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