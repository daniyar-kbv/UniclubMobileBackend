from django.template.defaultfilters import date as _date

from main.models import TelegramUser, Course, CourseReview

from telebot import types
import telebot, constants, datetime

bot = telebot.TeleBot(constants.TELEGRAM_BOT_TOKEN)
bot.set_webhook(url=constants.TELEGRAM_BOT_URL)


@bot.message_handler(commands=['start'])
def handle_start(message):
    # markup = types.InlineKeyboardMarkup()
    # key_view = types.InlineKeyboardButton(
    #     text='Просмотреть отзывы',
    #     callback_data='asd'
    # )
    # markup.add(key_view)
    # text = ')'
    # bot.send_message(message.from_user.id, text, reply_markup=markup)
    register_user(message.from_user)
    course_id = extract_course_id(message.text)
    main_menu(course_id, message.from_user.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    action = call.data.split()[0]
    course_id = int(call.data.split()[1])
    print('1')
    user = authorize_user(call.data.split()[2])
    print('(')
    try:
        course = Course.objects.get(id=course_id)
    except:
        bot.send_message(user.telegram_id, 'Занятие не найдено')
        return
    if action == constants.TELEGRAM_ACTION_VIEW_REVIEWS:
        from_ = int(call.data.split()[3]) if len(call.data.split()) > 3 else 0
        to_ = int(call.data.split()[4]) if len(call.data.split()) > 4 else 0
        reviews = course.reviews.all()[from_:to_]
        if reviews.count() > 0:
            for index, review in enumerate(reviews):
                if index != 9 or reviews[from_ + 10:to_ + 10].count == 0:
                    bot.send_message(user.telegram_id, serialize_review(review))
                else:
                    keyboard = types.InlineKeyboardMarkup()
                    key_more = types.InlineKeyboardButton(
                        text='Посмотреть еще',
                        callback_data=f'{constants.TELEGRAM_ACTION_VIEW_REVIEWS} {course_id} {user.telegram_id} {from_ + 10} {to_ + 10}'
                    )
                    key_back = types.InlineKeyboardButton(
                        text='Назад',
                        callback_data=f'{constants.TELEGRAM_ACTION_BACK} {course_id} {user.telegram_id}'
                    )
                    keyboard.add(key_more)
                    keyboard.add(key_back)
                    bot.send_message(user.telegram_id, serialize_review(review), reply_markup=keyboard)
        else:
            bot.send_message(user.telegram_id, 'К сожалению по данному занятию отсутвуют отзывы')
            main_menu(course_id, user.telegram_id)
    elif action == constants.TELEGRAM_ACTION_LEAVE_REVIEW:
        message = bot.send_message(user.telegram_id, 'Напишите ваш отзыв')
        bot.register_next_step_handler(message, leave_review, course_id)
    elif action == constants.TELEGRAM_ACTION_BACK:
        main_menu()


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
            markup = types.InlineKeyboardMarkup()
            key_view = types.InlineKeyboardButton(
                text='Просмотреть отзывы',
                callback_data=f'{constants.TELEGRAM_ACTION_VIEW_REVIEWS} {course_id} {user_id}'
            )
            key_leave = types.InlineKeyboardButton(
                text='Оставить отзыв',
                callback_data=f'{constants.TELEGRAM_ACTION_LEAVE_REVIEW} {course_id} {user_id}'
            )
            markup.add(key_view)
            markup.add(key_leave)
            text = f"""Занятие: {course.name}
            
Выберите действие"""
            bot.send_message(user_id, text, reply_markup=markup)
        except:
            bot.send_message(user_id, 'Занятие не найдено')
    else:
        bot.send_message(user_id, 'Занятие не найдено')


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