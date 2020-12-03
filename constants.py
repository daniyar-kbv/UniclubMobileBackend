DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

WEEKDAYS = (
    (MONDAY, 'Понедельник'),
    (TUESDAY, 'Вторник'),
    (WEDNESDAY, 'Среда'),
    (THURSDAY, 'Четверг'),
    (FRIDAY, 'Пятница'),
    (SATURDAY, 'Суббота'),
    (SUNDAY, 'Воскресенье'),
)

TIME_BEFORE_LUNCH = 'BEFORE_LUNCH'
TIME_AFTER_LUNCH = 'AFTER_LUNCH'
TIME_ALL_DAY = 'ALL_DAY'

TIMES = [
    TIME_BEFORE_LUNCH,
    TIME_AFTER_LUNCH,
    TIME_ALL_DAY
]

TELEGRAM_BOT_TOKEN = '1423817155:AAEz2djQyKkFeqDxGzsWBMUDbwSIYJdcxlQ'
TELEGRAM_BOT_URL = f'https://server.uniclub.kz/main/bot/'
TELEGRAM_DATETIME_FORMAT = '%d %B, %Y'

TELEGRAM_ACTION_VIEW_REVIEWS = 'view_reviews'
TELEGRAM_ACTION_LEAVE_REVIEW = 'leave_review'
TELEGRAM_ACTION_BACK = 'back'
