import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from os import getenv
import random

load_dotenv()

TOKEN = getenv("TOKEN")

win_words = ["выйгр", "выигра", "победил", "приз"]


def get_answer(message):
    if "заказ" in message.lower():
        return ("приветствуем👋\n"
                "Чтобы оформить заказ, пожалуйста, позвоните в ближайший филиал или воспользуйтесь нашим сайтом.\n\n"
                "☎Контакты филиалов: https://sushivostok.com/kontakty/\n\n"
                "🖥️Меню на нашем сайте: https://sushivostok.com/products/sety/\n\n"
                "⚠К сожалению, в группе ВКонтакте, мы технически не можем принять заказ")

    for keyword in win_words:
        if keyword in message.lower():
            return ("приветствуем👋\n"
                    "Если вы выиграли в нашем конкурсе, то, пожалуйста, позвоните в ближайший филиал и договоритесь "
                    "об изготовлении вашего подарочного сета. В качестве доказательства при получении приза, "
                    "предъявите публикацию с вашей победой на странице сообщества\n\n"
                    "☎Контакты филиалов: https://sushivostok.com/kontakty/")


# Инициализация VK API и авторизация
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Основной цикл бота
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        # Получаем информацию о пользователе, отправившем сообщение
        user_id = event.user_id
        user_info = vk.users.get(user_ids=user_id)[0]
        first_name = user_info['first_name']

        # Получаем текст сообщения
        message_text = event.text

        # Получаем ответ
        response = get_answer(message_text)

        # Формируем сообщение с использованием имени отправителя
        message = f"{first_name}, {response}"

        # Отправляем ответ с случайным идентификатором
        vk.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)  # Добавляем random_id
        )

