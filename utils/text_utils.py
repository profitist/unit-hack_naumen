from aiogram.types import Message


def send_start_common_user_message(message: Message):
    text = ('Привет! Я Бот - организатор мероприятий компании Naumen 😊\n\n'
            'Помогу тебе узнать всю информацию о предстоящих мероприятиях'
            'нашей компании, а также при желании зарегистрироваться на них.\n'
            'Ниже представлено главное меню ⬇️')
    return text


def send_start_admin_user_message(message: Message):
    text = (f'Привет, {message.from_user.username}!\n\n'
            f'🔐Ты попал в админку Бота - организатора мероприятий Naumen\n'
            f'Есть вопросы? отправь команду /admin_help\n\n'
            f'Ниже панель главного меню ⬇️\n\n'
            )
    return text


def send_notification_of_creating_event(data: dict):
    return (f'Новое событие 🔥🔥🔥\n\n'
            f'**{data["title"]}**\n\n'
            f'{data["description"]}\n\n'
            f'Когда: {data["date"]}\n'
            f'Места ограничены: {data["vacant_places"]}\n')


