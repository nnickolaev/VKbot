"""Модуль работы с фронтэндом бота
"""
import vk_api
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import date
from core import VkTools
from configg import access_token, community_token, access_token
from database import check_viewed, add_viewed, create_all, wipe_all


VkTool = VkTools(access_token)  # Создание экземпляра класса VkTools для работы с бэкэндом VK

class BotInterface:  # Класс для работы с фронтэндом VK

    def __init__(self, token):
        self.bot = vk_api.VkApi(token=token)
        self.bot_api = self.bot.get_api()
        self.longpoll = VkLongPoll(self.bot)  # Дописал чтобы использовать лонгпол в другой функции

    def message_send(self, user_id, message, attachment=None):  # Функция для отправки сообщений
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment
                         }
                        )

    # Пробую код для ввода возраста, если у пользователя отсутствует год рождения
    def ask_age(self, user_id):
        try:
            print('Полная дата рождения пользователя скрыта')
            self.message_send(user_id, 'Прошу ввести минимальный и максимальный возраст для поиска в формате: 18-50')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    global age_combination
                    age_combination = event.text
                    return self.format_age(user_id, age_combination)
        except KeyError:
            print('Возраст введен с ошибкой')
            self.message_send(user_id,
                              'Возраст введен с ошибкой. Прошу ввести минимальный и максимальный возраст для поиска в формате: 18-50')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age_combination = event.text
                    return self.format_age(user_id, age_combination)

    def format_age(self, user_id, age):
        global age_from, age_to
        ages = age.split('-')
        try:
            age_from = int(ages[0])
            age_to = int(ages[1])
            print(f'Возраст для поиска от {age_from} до {age_to}')
            return
        except ValueError:
            print('Возраст введен с ошибкой')
            return

    def ask_sex(self, user_id):
        try:
            print('Пол пользователя скрыт')
            self.message_send(user_id, 'Необходимо выбрать пол партнера для поиска, напишите М для поиска мужчины, либо Ж для поиска женщины')
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
                    city_id = self.bot_api.database.getCities(country_id=1, q=city_name)["items"][0]["id"]
                    return city_id
        except KeyError:
            print('Город введен с ошибкой')
            self.message_send(user_id,
                              'Город введен с ошибкой. Прошу ввести ввести город для поиска, например: Якутск')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    city_name = event.text
                    city_id = self.bot_api.database.getCities(country_id=1, q=city_name)["items"][0]["id"]
                    return city_id

    def handler(self):  # Функция для прослушивания, обработки и реагирования на входящие команды
        create_all()
        # longpoll = VkLongPoll(self.bot)  # Для подключения к Long Poll серверу VK
        for event in self.longpoll.listen():  # Прослушивание событий
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # Условие для работы с новыми сообщениями, приходящими боту
                request = event.text
                # Приветствие
                if request.lower() == 'привет':  # Условие для реакции на сообщение "Привет". Текст сообщения приводится в нижний регистр, для точности срабатывания условия
                    self.message_send(event.user_id, 'Добрый день! Для начала работы напишите слово "Поиск"')
                # Поиск профилей
                elif request.lower() =='поиск':  # Условие для реакции на команду "Поиск"
                    offset = 0
                    global info  # Делаю переменную глобальной, т.к. будет использоваться в других блоках
                    info = VkTool.get_profile_info(event.user_id)  # Получение информации о пользователе функцией из класса для работы с бэкэндом
                    birthday = info[0]['bdate']  # Для расчета возраста в анкетах беру возраст пользователя
                    f_birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y")  # Привожу дату рождения к формату
                    # Пробный код для получения возраста поиска от пользователя
                    print(f_birthday.year)
                    global age_from
                    global age_to
                    if not f_birthday.year:
                        self.ask_age(event.user_id)
                    else:
                        today = date.today()  # Получаю текущую дату для дальнейшего вычисления возраста пользователя
                        age = today.year - f_birthday.year  # Вычисление возраста пользователя
                        if age >= 24:  # Это условие введено, чтобы не отображались несовершеннолетние профили
                            age_from = age - 5  # Возраст "от". Оптимальная разница в возрасте для пар +- 5 лет
                        else:
                            age_from = 18
                        age_to = age + 5  # Возраст "до"

                    # Далее расчет данных для поиска: возраст от, возраст до, пол
                    # Backup
                    # f_birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y")  # Привожу дату рождения к формату
                    # today = date.today()  # Получаю текущую дату для дальнейшего вычисления возраста пользователя
                    # age = today.year - f_birthday.year  # Вычисление возраста пользователя
                    # if age >= 24:  # Это условие введено, чтобы не отображались несовершеннолетние профили
                    #     global age_from  # Аналогично списку info, делаю переменную глобальной для дальнейшего использования в других блоках
                    #     age_from = age - 5  # Возраст "от". Оптимальная разница в возрасте для пар +- 5 лет
                    # else:
                    #     age_from = 18
                    # global age_to
                    # age_to = age + 5  # Возраст "до"
                    global sex
                    if not info[0]['sex']:
                        sex = self.ask_sex(event.user_id)
                    elif info[0]['sex'] == 1: # Автоматическая инверсия пола для подбора традиционного партнера
                        sex = 2  # Женщинам ищется мужчина
                    else:
                        sex = 1  # Мужчинам ищется женщина

                    if 'city' in info:
                        city_id = info[0]['city']['id']
                    else:
                        city_id = self.ask_city(event.user_id)

                    global recieved_profiles
                    recieved_profiles = VkTool.user_search(city_id, age_from, age_to, sex)  # Получаю список пользователей по заданным параметрам
                    current_profile = recieved_profiles.pop(0)  # Заношу в переменную первый профиль из списка, попутно удаляя его из него
                    while check_viewed(event.user_id, current_profile['id']):  # Вызываю цикл с проверкой был ли профиль просмотрен. Цикл будет срабатывать пока не найдется не просмотренный профиль
                        if len(recieved_profiles) == 0:  # Проверка не закончился ли список
                            recieved_profiles = VkTool.user_search_offset(info[0]['city']['id'], age_from, age_to, sex)  # Если список закончился, то получаю новых пользователей со сдвигом
                        if len(recieved_profiles) > 0:  # Если список не закончился. За счет "if", вместо "elif" эта проверка срабатывает вне зависимости от предыдущей
                            current_profile = recieved_profiles.pop(0)  # Заношу в переменную следующий профиль и цикл проверки на просмотр начинается снова

                    add_viewed(event.user_id, current_profile['id'])  # Добавляю профиль в таблицу "Viewed"
                    photos = VkTool.photos_get(current_profile['id'])  # Формирую attachment с тремя лучшими фотографиями
                    message = f"""Найден пользователь: {current_profile['name']}
                        Ссылка на страницу: {current_profile['link']} 
                        Отправьте "Далее", чтобы получить следующий профиль"""  # Формирую сообщение именем, ссылкой и фото для отправки
                    self.message_send(event.user_id, message, photos)
                # Поиск следующего профиля
                elif request.lower() == 'далее':  # Условие для реакции на команду "Далее"
                    while check_viewed(event.user_id, current_profile['id']):  # Проверка на просмотренность
                        if len(recieved_profiles) == 0:  # Проверка не закончился ли список
                            recieved_profiles = VkTool.user_search_offset(info[0]['city']['id'], age_from, age_to, sex)  # Запрос новых профилей со сдвигом
                        if len(recieved_profiles) > 0:  # Проверка списка на наличие профилей
                            current_profile = recieved_profiles.pop(0)  # Выбор профиля и удаление его из списка
                    add_viewed(event.user_id, current_profile['id'])  # Добавляю профиль в таблицу
                    photos = VkTool.photos_get(current_profile['id'])  # Формирую attachment
                    message = f"""Найден пользователь: {current_profile['name']} 
                        Ссылка на страницу: {current_profile['link']} 
                        Отправьте "Далее", чтобы получить следующий профиль""" # Формирую сообщение
                    self.message_send(event.user_id, message, photos)
                # Сброс просмотренных профилей, чтобы снова попадались в поиске
                elif request.lower() == 'сброс':  # Условие для реакции на команду "Сброс"
                    wipe_all()  # Вызываю функцию очистки Базы данных
                    self.message_send(event.user_id, 'Просмотренные профили сброшены!')
                # Прощание
                elif request.lower() == 'пока':  # Условие для реакции на команду "Пока"
                    self.message_send(event.user_id, 'Пока!')
                # Подсказка с командами
                elif request.lower() == 'помощь':  # Условие для реакции на команду "Помощь"
                    self.message_send(event.user_id, """Список команд:
                    Поиск - начать поиск подходящих профилей
                    Далее - получить следующий профиль
                    Сброс - сброс просмотренных профилей 
                    Помощь - получить список команд""")
                # Обработка непредусмотренных сообщений
                else:
                    self.message_send(event.user_id, 'Неизвестная команда. Напишите "Помощь", чтобы посмотреть список команд')


if __name__ == '__main__':
    bot1 = BotInterface(community_token)
    # Отправить фотографию
    # media = f'photo694200998_457239019'
    # media = ','.join(['photo3359699_282707429', 'photo3359699_334184265', 'photo3359699_266808377'])
    # bot.message_send(3359699, 'фото', attachment=media)

    # Проверка ответов на сообщения
    # bot1.handler()

    # Проверка поиска id города
    cityid = bot1.bot_api.database.getCities(country_id=1, q='Владивосток')  # ["items"][0]["id"]
    print(cityid)

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