"""Модуль работы с фронтэндом бота
"""
import vk_api
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import date
from core import VkTools
from config import access_token
from database import check_viewed, add_viewed, create_all, wipe_all


VkTool = VkTools(access_token)


class BotInterface:

    def __init__(self, token):
        self.bot = vk_api.VkApi(token=token)
        self.bot_api = self.bot.get_api()
        self.longpoll = VkLongPoll(self.bot)
        self.age_from = None
        self.age_to = None

    def message_send(self, user_id, message, attachment=None):
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment
                         }
                        )

    def ask_age(self, user_id):
        try:
            print('Полная дата рождения пользователя скрыта')
            self.message_send(user_id, 'Прошу ввести минимальный и максимальный возраст для поиска в формате: 18-50')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age_combination = event.text
                    return self.format_age(user_id, age_combination)
        except KeyError:
            print('Возраст введен с ошибкой')
            self.message_send(user_id,
                              'Возраст введен с ошибкой. Прошу ввести минимальный и максимальный возраст для поиска в '
                              'формате: 18-50')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age_combination = event.text
                    return self.format_age(user_id, age_combination)

    def format_age(self, user_id, age):
        ages = age.split('-')
        try:
            self.age_from = int(ages[0])
            self.age_to = int(ages[1])
            print(f'Возраст для поиска от {self.age_from} до {self.age_to}')
            return
        except ValueError:
            print('Возраст введен с ошибкой')
            return

    def ask_sex(self, user_id):
        try:
            print('Пол пользователя скрыт')
            self.message_send(user_id, 'Необходимо выбрать пол партнера для поиска, напишите М для поиска мужчины, '
                                       'либо Ж для поиска женщины')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text.lower() == 'м':
                        return 2
                    elif event.text.lower() == 'ж':
                        return 1
        except KeyError:
            print('Пол введен с ошибкой')
            self.message_send(user_id,
                              'Пол введен с ошибкой. Прошу написать М для поиска мужчины, либо Ж для поиска женщины')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text.lower() == 'м':
                        return 2
                    elif event.text.lower() == 'ж':
                        return 1

    def ask_city(self, user_id):
        try:
            print('Город пользователя скрыт')
            self.message_send(user_id, 'Прошу ввести город для поиска')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    city_name = event.text
                    city_id = VkTool.city_name_to_id(city_name)
                    return city_id
        except KeyError:
            print('Город введен с ошибкой')
            self.message_send(user_id,
                              'Город введен с ошибкой. Прошу ввести ввести город для поиска, например: Якутск')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    city_name = event.text
                    city_id = VkTool.city_name_to_id(city_name)
                    return city_id

    def handler(self):
        create_all()
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                if request.lower() == 'привет':
                    self.message_send(event.user_id, 'Добрый день! Для начала работы напишите слово "Поиск"')
                elif request.lower() =='поиск':
                    info = VkTool.get_profile_info(event.user_id)
                    birthday = info[0]['bdate']
                    f_birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y")
                    print(f_birthday.year)
                    if not f_birthday.year:
                        self.ask_age(event.user_id)
                    else:
                        today = date.today()
                        age = today.year - f_birthday.year
                        if age >= 24:
                            self.age_from = age - 5
                        else:
                            self.age_from = 18
                        self.age_to = age + 5

                    if not info[0]['sex']:
                        sex = self.ask_sex(event.user_id)
                    elif info[0]['sex'] == 1:
                        sex = 2
                    else:
                        sex = 1

                    if 'city' in info:
                        city_id = info[0]['city']['id']
                    else:
                        city_id = self.ask_city(event.user_id)

                    recieved_profiles = VkTool.user_search(city_id, self.age_from, self.age_to, sex)
                    current_profile = recieved_profiles.pop(0)
                    while check_viewed(event.user_id, current_profile['id']):
                        if len(recieved_profiles) == 0:
                            recieved_profiles = VkTool.user_search_offset(info[0]['city']['id'], self.age_from, self.age_to, sex)
                        if len(recieved_profiles) > 0:
                            current_profile = recieved_profiles.pop(0)

                    add_viewed(event.user_id, current_profile['id'])
                    photos = VkTool.photos_get(current_profile['id'])
                    message = f"""Найден пользователь: {current_profile['name']}
                        Ссылка на страницу: {current_profile['link']} 
                        Отправьте "Далее", чтобы получить следующий профиль"""
                    self.message_send(event.user_id, message, photos)
                elif request.lower() == 'далее':
                    while check_viewed(event.user_id, current_profile['id']):
                        if len(recieved_profiles) == 0:
                            recieved_profiles = VkTool.user_search_offset(info[0]['city']['id'], self.age_from, self.age_to, sex)
                        if len(recieved_profiles) > 0:
                            current_profile = recieved_profiles.pop(0)
                    add_viewed(event.user_id, current_profile['id'])
                    photos = VkTool.photos_get(current_profile['id'])
                    message = f"""Найден пользователь: {current_profile['name']} 
                        Ссылка на страницу: {current_profile['link']} 
                        Отправьте "Далее", чтобы получить следующий профиль"""
                    self.message_send(event.user_id, message, photos)
                elif request.lower() == 'сброс':
                    wipe_all()
                    self.message_send(event.user_id, 'Просмотренные профили сброшены!')
                elif request.lower() == 'пока':
                    self.message_send(event.user_id, 'Пока!')
                elif request.lower() == 'помощь':
                    self.message_send(event.user_id, """Список команд:
                    Поиск - начать поиск подходящих профилей
                    Далее - получить следующий профиль
                    Сброс - сброс просмотренных профилей 
                    Помощь - получить список команд""")
                else:
                    self.message_send(event.user_id, 'Неизвестная команда. Напишите "Помощь", чтобы посмотреть список '
                                                     'команд')
