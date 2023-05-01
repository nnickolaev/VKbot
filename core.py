import datetime

import vk_api
from config import access_token
from vk_api.exceptions import ApiError
# from database import check_viewed
#from datetime import datetime
from datetime import date


class VkTools:
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)

    def get_profile_info(self, user_id):
        try:
            info = self.ext_api.method('users.get',
                                       {'user_id': user_id,
                                        'fields': 'bdate,city,sex,relation'
                                        }
                                       )
        except ApiError:
            return
        return info

    def user_search(self, city_id, age_from, age_to, sex, offset=None):

        try:
            profiles_list = self.ext_api.method('users.search',
                                           {'city_id': city_id,
                                            'age_from': age_from,
                                            'age_to': age_to,
                                            'sex': sex,
                                            'count': 30,
                                            'offset': offset
                                            })

            profiles_list = profiles_list['items']  # Чтобы фильтровать закрытые профили

            result = []

            # Проверка на открытость аккаунта
            for profile in profiles_list:
                if not profile['is_closed']:
                    result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                                   'id': profile['id']
                                   })

            result_checked = []

            # Проверка на наличие в БД
            for profile in result:
                if check_viewed(profile['id']):
                    result_checked.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                                           'id': profile['id']
                                           })
            return result_checked

        except ApiError:
            print(ApiError)


    # profiles_list = profiles_list['items']  # Чтобы фильтровать закрытые профили
    #
    # result = []
    # for profile in profiles_list:
    #     if not profile['is_closed']:
    #         result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
    #                        'id': profile['id']
    #                        })
    #
    # return result

    # def photos_get(self, owner_id):
    #     photos = self.ext_api.method('photos.get',
    #                                  {'album_id': 'profile',
    #                                   'owner_id': owner_id,
    #                                   'extended': 1,
    #                                   'offset': 0
    #                                   })
    #     try:
    #         photos_list = photos['items']
    #     except KeyError:
    #         return
    #     else:
    #         photos_sorted = [(item['likes'], f'photo{item['owner_id']}_{item['id']}') for item in photos_list]
    #         photos_sorted = sorted(photos_sorted, reverse=True)
    #         photos_sorted = [item[1] for item in photos_sorted][:3]
    #         return photos_sorted

        # result = []
        # for num, photo in enumerate(photos_list):
        #     result.append({'owner_id': photo['owner_id'],
        #                    'id': photo['id']
        #                    })
        #     if num == 2:  # Чтобы выбирались три фотографии. Нужно еще допилить, чтобы выбирались 3 самые популярные
        #         break
        #
        # return result
        # photos_list = [{'owner_id': 709972942, 'id': 457239017}]
        # media_id = []
        # for item in photos_list:
        #     for value in item:
        #         media_id.append(item[value])
        # media = f'photo{media_id[0]}_{media_id[1]}'


    def photos_get(self, owner_id):
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
        for photo in photos:
            result.append([photo['likes']['count'], f"photo{photo['owner_id']}_{photo['id']}"])
        result = sorted(result, reverse=True)
        result = [item[1] for item in result][:3]
        result = ','.join(result)
        # for num, photo in enumerate(photos):
        #     result.append({'owner_id': photo['owner_id'],
        #                    'id': photo['id'],
        #                    'likes': photo['likes']
        #                    })
        #
        #
        #     if num == 2:  # Чтобы выбирались три фотографии. Нужно еще допилить, чтобы выбирались 3 самые популярные
        #         break
        return result


    def get_user_from_search():
        user_from_search = 0


        return user_from_search

    # Backup
    # def photos_get(self, user_id):
    #     photos = self.ext_api.method('photos.get',
    #                                  {'album_id': 'profile',
    #                                   'owner_id': user_id
    #                                   })
    #     try:
    #         photos = photos['items']
    #     except KeyError:
    #         return
    #
    #     result = []
    #     for num, photo in enumerate(photos):
    #         result.append({'owner_id': photo['owner_id'],
    #                        'id': photo['id']
    #                        })
    #         if num == 2:  # Чтобы выбирались три фотографии. Нужно еще допилить, чтобы выбирались 3 самые популярные
    #             break
    #
    #     return result


if __name__ == '__main__':
    #tools = VkTools(access_token)

    # Проверка получения данных пользователя
    # info = tools.get_profile_info(3359699)
    # if info:
    #     print(tools.get_profile_info(3359699))
    # else:
    #     pass
    # Результат в виде: [{'id': 3359699, 'bdate': '17.12.1989', 'city': {'id': 168, 'title': 'Якутск'},
    # 'relation': 4, 'sex': 2, 'first_name': 'Николай', 'last_name': 'Николаев',
    # 'can_access_closed': True, 'is_closed': False}]

    info = [{'id': 3359699, 'bdate': '17.12.1989', 'city': {'id': 168, 'title': 'Якутск'}, 'relation': 4, 'sex': 2, 'first_name': 'Николай', 'last_name': 'Николаев', 'can_access_closed': True, 'is_closed': False}]
    birthday = info[0]['bdate']
    f_birthday = datetime.datetime.strptime(birthday, "%d.%m.%Y")
    today = date.today()
    age = today.year - f_birthday.year
    if age >= 24:
        age_from = age - 5
    else:
        age_from = 18
    # print(birthday)
    # print(f_birthday)
    # print(today)
    # print(age)
    # print(age_from)
    print(info[0]['city']['id'])
    print(info[0]['sex'])


    # Проверка поиска пользователей
    # profiles = tools.user_search(1, 20, 40, 1)
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
