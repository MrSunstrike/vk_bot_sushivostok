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
        return ("Здравствуйте. Для заказа, пожалуйста, позвоните в ближайший "
                "филиал. Или можете оставить заявку на сайте сушивосток.рф и "
                "вам перезвонит оператор\nК сожалению, мы не принимаем заказы "
                "в социальных сетях:(")
    for keyword in win_words:
        if keyword in message.lower():
            return ("Добрый день. Если вы выиграли в нашем конкурсе, то, "
                    "пожалуйста, позвоните в ближайший филиал и договоритесь об "
                    "изготовлении вашего подарочного сета. В качестве "
                    "доказательства при получении приза, предъявите это "
                    "сообщение:)")


# Инициализация VK API и авторизация
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Основной цикл бота
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        # Получаем текст сообщения
        message_text = event.text

        # Получаем ответ
        response = get_answer(message_text)

        # Отправляем ответ с случайным идентификатором
        vk.messages.send(
            user_id=event.user_id,
            message=response,
            random_id=random.randint(1, 1000)  # Добавляем random_id
        )
