import vk_api
import datetime

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import date
from core import VkTools
from config import access_token, community_token
from database import check_viewed, add_viewed, create_all

VkTool = VkTools(community_token)

class BotInterface:

    def __init__(self, token):
        self.bot = vk_api.VkApi(token=token)

    def message_send(self, user_id, message, attachment=None):
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment
                         }
                        )

    def handler(self):
        create_all()
        longpoll = VkLongPoll(self.bot)
        viewed_list = []
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                if request.lower() == 'привет':
                    self.message_send(event.user_id, 'Добрый день! Для начала работы напишите слово "Поиск", для просмотра следующей анкеты, напишите слово "Далее"')
                elif request.lower() =='поиск':
                    info = VkTools.get_profile_info(event.user_id)

                    birthday = info[0]['bdate']
                    f_birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y")
                    today = date.today()
                    age = today.year - f_birthday.year
                    if age >= 24:
                        age_from = age - 5
                    else:
                        age_from = 18
                    age_to = age + 5

                    recieved_profiles = VkTool.user_search(info[0]['city']['id'], age_from, age_to, info[0]['sex'])
                    for recieved_profile in recieved_profiles:
                        if not check_viewed(event.user_id, recieved_profile['id']):
                            add_viewed(event.user_id, recieved_profile['id'])


                        else:
                            continue

                elif request.lower() == 'далее':
                    pass
                elif request.lower() == 'пока':
                    self.message_send(event.user_id, 'Пока!')
                # Для проверки:
                elif request.lower() == 'фото':
                    self.message_send(event.user_id, 'Отправляю фото', 'photo712335667_457240249')
                else:
                    self.message_send(event.user_id, 'Неизвестная команда')


        # print(event.text)


if __name__ == '__main__':
    bot = BotInterface(community_token)
    # Отправить фотографию
    # media = f'photo694200998_457239019'
    media = ','.join(['photo3359699_282707429', 'photo3359699_334184265', 'photo3359699_266808377'])
    bot.message_send(3359699, 'фото', attachment=media)

    # Проверка ответов на сообщения
    # bot.handler()

