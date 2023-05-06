import vk_api
import datetime

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import date
from core import VkTools
from config import access_token, community_token, access_token
from database import check_viewed, add_viewed, create_all

# VkTool = VkTools(community_token)
# Проверка. Не понял почему было community_token, пробую access_token
VkTool = VkTools(access_token)

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
        offset = 0
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                if request.lower() == 'привет':
                    self.message_send(event.user_id, 'Добрый день! Для начала работы напишите слово "Поиск", для просмотра следующей анкеты, напишите слово "Далее"')
                elif request.lower() =='поиск':
                    offset = 0
                    global info
                    info = VkTool.get_profile_info(event.user_id)
                    birthday = info[0]['bdate']
                    f_birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y")
                    today = date.today()
                    age = today.year - f_birthday.year
                    if age >= 24:
                        global age_from
                        age_from = age - 5
                    else:
                        age_from = 18
                    global age_to
                    age_to = age + 5
                    global sex
                    if info[0]['sex'] == 1:
                        sex = 2
                    else:
                        sex = 1
                    # print(info[0]['city']['id'], age_from, age_to, sex)
                    global recieved_profiles
                    recieved_profiles = VkTool.user_search(info[0]['city']['id'], age_from, age_to, sex)
                    # print(recieved_profiles)

                    # Изначальный код
                    # for recieved_profile in recieved_profiles:
                        # if not check_viewed(event.user_id, recieved_profile['id']):
                        #     add_viewed(event.user_id, recieved_profile['id'])
                        #     photos = VkTool.photos_get(recieved_profile['id'])
                        #
                        #     self.message_send(event.user_id, f"Найден пользователь: {recieved_profile['name']}", photos)
                        # else:
                        #     continue

                    # Пробую видоизменить логику, попытка 100
                    # if recieved_profiles:
                    #     answer = False
                    #     while not answer:
                    #         current_profile = recieved_profiles.pop(0)
                    #         if not check_viewed(event.user_id, current_profile['id']):
                    #             photos = VkTool.photos_get(current_profile['id'])
                    #             self.message_send(event.user_id, f"Найден пользователь: {current_profile['name']}", photos)
                    #             answer = True
                    #             break
                    #     if not recieved_profiles:
                    #
                    # else:
                    #     recieved_profiles = VkTool.user_search(info[0]['city']['id'], age_from, age_to, sex, 30)
                    # continue

                    # С очередной логикой все плохо, поэтому пробую новую
                    if len(recieved_profiles) == 0:
                        offset += 30
                        recieved_profiles = VkTool.user_search(info[0]['city']['id'], age_from, age_to, sex, offset)
                    else:
                        current_profile = recieved_profiles.pop(0)
                        while check_viewed(event.user_id, current_profile['id']):
                            current_profile = recieved_profiles.pop(0)
                        add_viewed(event.user_id, current_profile['id'])
                        photos = VkTool.photos_get(current_profile['id'])
                        message = f"""Найден пользователь: {current_profile['name']} 
                            Ссылка на страницу: {current_profile['link']} 
                            Отправьте "Далее", чтобы получить следующий профиль"""
                        self.message_send(event.user_id, message, photos)
                elif request.lower() == 'далее':
                    if len(recieved_profiles) == 0:
                        offset += 30
                        recieved_profiles = VkTool.user_search(info[0]['city']['id'], age_from, age_to, sex, offset)
                    else:
                        current_profile = recieved_profiles.pop(0)
                        while check_viewed(event.user_id, current_profile['id']):
                            current_profile = recieved_profiles.pop(0)
                        add_viewed(event.user_id, current_profile['id'])
                        photos = VkTool.photos_get(current_profile['id'])
                        message = f"""Найден пользователь: {current_profile['name']} 
                            Ссылка на страницу: {current_profile['link']} 
                            Отправьте "Далее", чтобы получить следующий профиль"""
                        self.message_send(event.user_id, message, photos)
                elif request.lower() == 'пока':
                    self.message_send(event.user_id, 'Пока!')
                # Для проверки:
                elif request.lower() == 'помощь':
                    self.message_send(event.user_id, '''Список команд:
                    Поиск - начать поиск подходящих профилей
                    Далее - получить следующий профиль
                    Помощь - получить список команд''')
                else:
                    self.message_send(event.user_id, 'Неизвестная команда. Напишите "Помощь", чтобы посмотреть список команд')


        # print(event.text)


if __name__ == '__main__':
    bot = BotInterface(community_token)
    # Отправить фотографию
    # media = f'photo694200998_457239019'
    # media = ','.join(['photo3359699_282707429', 'photo3359699_334184265', 'photo3359699_266808377'])
    # bot.message_send(3359699, 'фото', attachment=media)

    # Проверка ответов на сообщения
    bot.handler()

    # Проверка получения данных пользователя
    # user = VkTool.get_profile_info(3359699)
    # print(user)

    # Проверка получения профилей
    # city = 168  # Якутск
    # age_from = 29
    # age_to = 39
    # sex = 1
    #
    # user_search = VkTool.user_search(city, age_from, age_to, sex)
    # print(user_search)

    # Проверка моей новой логики
    # recieved_profiles = []
    # current_profile = recieved_profiles.pop(0)
    # if not check_viewed(123, current_profile['id']):
    #     photos = VkTool.photos_get(current_profile['id'])
    #     print(f"Найден пользователь: {current_profile['name']}")
    #     # self.message_send(event.user_id, f"Найден пользователь: {current_profile['name']}", photos)
    # else:
    #     current_profile = recieved_profiles.pop(0)
    #     photos = VkTool.photos_get(current_profile['id'])
    #     print(f"Найден пользователь: {current_profile['name']}")