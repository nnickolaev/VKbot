"""Модуль работы с фронтэндом бота
"""
import vk_api
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import date
from core import VkTools
from config import access_token, community_token, access_token
from database import check_viewed, add_viewed, create_all, wipe_all


VkTool = VkTools(access_token)  # Создание экземпляра класса VkTools для работы с бэкэндом VK

class BotInterface:  # Класс для работы с фронтэндом VK

    def __init__(self, token):
        self.bot = vk_api.VkApi(token=token)

    def message_send(self, user_id, message, attachment=None):  # Функция для отправки сообщений
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment
                         }
                        )

    def handler(self):  # Функция для прослушивания, обработки и реагирования на входящие команды
        create_all()
        longpoll = VkLongPoll(self.bot)  # Для подключения к Long Poll серверу VK
        for event in longpoll.listen():  # Прослушивание событий
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
                    # Далее расчет данных для поиска: возраст от, возраст до, пол
                    f_birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y")  # Привожу дату рождения к формату
                    today = date.today()  # Получаю текущую дату для дальнейшего вычисления возраста пользователя
                    age = today.year - f_birthday.year  # Вычисление возраста пользователя
                    if age >= 24:  # Это условие введено, чтобы не отображались несовершеннолетние профили
                        global age_from  # Аналогично списку info, делаю переменную глобальной для дальнейшего использования в других блоках
                        age_from = age - 5  # Возраст "от". Оптимальная разница в возрасте для пар +- 5 лет
                    else:
                        age_from = 18
                    global age_to
                    age_to = age + 5  # Возраст "до"
                    global sex
                    if info[0]['sex'] == 1: # Автоматическая инверсия пола для подбора традиционного партнера
                        sex = 2  # Женщинам ищется мужчина
                    else:
                        sex = 1  # Мужчинам ищется женщина
                    global recieved_profiles
                    recieved_profiles = VkTool.user_search(info[0]['city']['id'], age_from, age_to, sex)  # Получаю список пользователей по заданным параметрам
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