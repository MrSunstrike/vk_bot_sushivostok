import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from os import getenv
import random

load_dotenv()

TOKEN = getenv("TOKEN")

win_words = ["выйгр", "выигра", "победил", "приз"]
ny_words = ["предзаказ", "новый год"]


def get_answer(message):
    for keyword in ny_words:
        if keyword in message.lower():
            return ("🎄Если вы хотите заказать роллы от Суши Восток к Новому году на 31 декабря, то мы настоятельно "
                    "рекомендуем оставить предзаказ в ближайшем филиале.\n\n"
                    "❗Важно, что 30 и 31 декабря филиалы будут работать исключительно по предзаказам, а совсем скоро "
                    "филиалы уже не смогут принимать даже предзаказы. Поторопитесь!\n\n"
                    "☎Контакты филиалов: https://sushivostok.com/kontakty/")

    if "заказ" in message.lower():
        return ("Чтобы оформить заказ, пожалуйста, позвоните в ближайший филиал или воспользуйтесь нашим сайтом.\n\n"
                "☎Контакты филиалов: https://sushivostok.com/kontakty/\n\n"
                "🖥️Меню на нашем сайте: https://sushivostok.com/products/sety/\n\n"
                "❗К сожалению, в группе ВКонтакте мы технически не можем принять заказ")

    for keyword in win_words:
        if keyword in message.lower():
            return ("Если вы выиграли в нашем конкурсе, то, пожалуйста, позвоните в ближайший филиал и договоритесь "
                    "об изготовлении вашего подарочного сета.\n\nВ качестве доказательства при получении приза, "
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
        message = f"{first_name}, приветствуем👋\n{response}"

        # Отправляем ответ с случайным идентификатором
        vk.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)  # Добавляем random_id
        )

