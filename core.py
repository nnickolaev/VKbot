"""Модуль работы с бэкэндом VK
"""
import vk_api
from vk_api.exceptions import ApiError
from config import access_token


# Класс для работы с backend VK
class VkTools:
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)

    def get_profile_info(self, user_id):  # Функция для получения данных о пользователе
        try:
            info = self.ext_api.method('users.get',
                                       {'user_id': user_id,
                                        'fields': 'bdate,city,sex,relation'
                                        }
                                       )
        except ApiError:
            return
        return info

    def user_search(self, city_id, age_from, age_to, sex, offset=None):  # Функция для поиска профилей
        try:
            profiles_list = self.ext_api.method('users.search',
                                           {'city_id': city_id,
                                            'age_from': age_from,
                                            'age_to': age_to,
                                            'sex': sex,
                                            'count': 30,  # Будет получено 30 пользователей
                                            'offset': offset
                                            })

            profiles_list = profiles_list['items']  # Чтобы фильтровать закрытые профили
            result = []

            for profile in profiles_list:  # Проверка на открытость аккаунта
                if not profile['is_closed']:
                    result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                                   'id': profile['id'],
                                   'link': 'vk.com/id'+str(profile['id'])
                                   })
            return result
        except ApiError:
            print(ApiError)

    def user_search_offset(self, city_id, age_from, age_to, sex):  # Функция для получения профилей со сдвигом
        offset = 0
        offset += 30
        recieved_profiles = self.user_search(city_id, age_from, age_to, sex, offset)
        return recieved_profiles

    def photos_get(self, owner_id):  # Функция для получения трех лучших фотографий профиля
        photos = self.ext_api.method('photos.get',
                                     {'album_id': 'profile',
                                      'owner_id': owner_id,
                                      'extended': 1
                                      })
        try:
            photos = photos['items']
        except KeyError:
            return

        result = []
        for photo in photos:  # Итерация по полученным фото и запись их в список
            result.append([photo['likes']['count'], f"photo{photo['owner_id']}_{photo['id']}"])  # Первым записываю количество лайков, чтобы потом отсортировать
        result = sorted(result, reverse=True)  # Сортировка по количеству лайков
        result = [item[1] for item in result][:3]  # Отбираю 3 лучших
        result = ','.join(result)  # Привожу к формату, который можно сразу отправить в attachment сообщения
        return result


if __name__ == '__main__':

    tools = VkTools(access_token)

    # Проверка получения данных пользователя
    # info = tools.get_profile_info(3359699)
    # if info:
    #     print(tools.get_profile_info(3359699))
    # else:
    #     pass
    # Результат в виде: [{'id': 3359699, 'bdate': '17.12.1989', 'city': {'id': 168, 'title': 'Якутск'},
    # 'relation': 4, 'sex': 2, 'first_name': 'Николай', 'last_name': 'Николаев',
    # 'can_access_closed': True, 'is_closed': False}]

    # Проба расчета age_from и age_to из расчета +-5 лет
    # info = [{'id': 3359699, 'bdate': '17.12.1989', 'city': {'id': 168, 'title': 'Якутск'}, 'relation': 4, 'sex': 2, 'first_name': 'Николай', 'last_name': 'Николаев', 'can_access_closed': True, 'is_closed': False}]
    # birthday = info[0]['bdate']
    # f_birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y")
    # today = date.today()
    # age = today.year - f_birthday.year
    # if age >= 24:
    #     age_from = age - 5
    # else:
    #     age_from = 18
    # print(birthday)
    # print(f_birthday)
    # print(today)
    # print(age)
    # print(age_from)
    # print(info[0]['city']['id'])
    # print(info[0]['sex'])


    # Проверка поиска пользователей
    # profiles = tools.user_search(1, 20, 40, 1)
    # print(profiles)
    # Результат: [{'name': 'Дарья Краснова', 'id': 41575774}, {'name': 'Екатерина Лачкова', 'id': 694200998},
    # {'name': 'Марк Цукерберг', 'id': 586676885}, {'name': 'Саргылана Аммосова', 'id': 19176824}, {'name': 'Айсена
    # Сыроватская-Лукина', 'id': 11675448}, {'name': 'Анна Булеева', 'id': 683840848}, {'name': 'Анна Колесникова',
    # 'id': 8395091}, {'name': 'Ангелина Козлова', 'id': 621038393}, {'name': 'Татьяна Пинигина', 'id': 25438994},
    # {'name': 'Татьяна Чекурова', 'id': 11815041}, {'name': 'Svetlana Semenova', 'id': 2263481}, {'name': 'Юлия
    # Сокольникова', 'id': 1980325}, {'name': 'Наталья Евсеева', 'id': 25601135}, {'name': 'Надежда Козловская',
    # 'id': 1328708}, {'name': 'Valerka Neobutova', 'id': 135612510}, {'name': 'Лена Буркина', 'id': 133385809},
    # {'name': 'Ксения Кириковна', 'id': 33822227}, {'name': 'Екатерина Уваровская', 'id': 5344442}, {'name': 'Инга
    # Ядреева', 'id': 10801559}, {'name': 'Айталина Афанасьева', 'id': 14187099}]

    # Проверка получения профилей
    # city = 168  # Якутск
    # age_from = 29
    # age_to = 39
    # sex = 1
    #
    # user_search = tools.user_search(city, age_from, age_to, sex)
    # print(user_search)


    # Проверка получения id из списка полученного методом .user_search()
    # profiles = [{'name': 'Дарья Краснова', 'id': 321}, {'name': 'Екатерина Лачкова', 'id': 694200998}, {'name': 'Марк Цукерберг', 'id': 586676885}, {'name': 'Саргылана Аммосова', 'id': 19176824}, {'name': 'Айсена Сыроватская-Лукина', 'id': 11675448}, {'name': 'Анна Булеева', 'id': 683840848}, {'name': 'Анна Колесникова', 'id': 8395091}, {'name': 'Ангелина Козлова', 'id': 621038393}, {'name': 'Татьяна Пинигина', 'id': 25438994}, {'name': 'Татьяна Чекурова', 'id': 11815041}, {'name': 'Svetlana Semenova', 'id': 2263481}, {'name': 'Юлия Сокольникова', 'id': 1980325}, {'name': 'Наталья Евсеева', 'id': 25601135}, {'name': 'Надежда Козловская', 'id': 1328708}, {'name': 'Valerka Neobutova', 'id': 135612510}, {'name': 'Лена Буркина', 'id': 133385809}, {'name': 'Ксения Кириковна', 'id': 33822227}, {'name': 'Екатерина Уваровская', 'id': 5344442}, {'name': 'Инга Ядреева', 'id': 10801559}, {'name': 'Айталина Афанасьева', 'id': 14187099}]
    # print(profiles[0]['id'])
    # profiles.pop(0)
    # for profile in profiles:
    #     if check_viewed(123, profile['id']) is True:
    #         # profiles.remove(profile)
    #         profiles.pop(0)
    #         print(profiles)
    # print(profiles)

    # Проверка получения данных о профиле
    # print(tools.get_profile_info(3359699))

    # Проверка получения трех фотографий
    # photos = tools.photos_get(3359699)
    # print(photos)  # вывод [{'owner_id': 709972942, 'id': 457239017}]

    # Получение медиавложения
    # photos_list = [{'owner_id': 709972942, 'id': 457239017}]
    # media_id = []
    # for item in photos_list:
    #     for value in item:
    #         media_id.append(item[value])
    # media = f'photo{media_id[0]}_{media_id[1]}'
    # print(media)
