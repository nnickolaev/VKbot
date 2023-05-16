"""Модуль работы с бэкэндом VK
"""
import vk_api
from vk_api.exceptions import ApiError


"""Класс для работы с backend VK
"""


class VkTools:
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)
        self.ext_get_api = self.ext_api.get_api()

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

            profiles_list = profiles_list['items']
            result = []

            for profile in profiles_list:
                if not profile['is_closed']:
                    result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                                   'id': profile['id'],
                                   'link': 'vk.com/id'+str(profile['id'])
                                   })
            return result
        except ApiError:
            print(ApiError)

    def user_search_offset(self, city_id, age_from, age_to, sex):
        offset = 0
        offset += 30
        recieved_profiles = self.user_search(city_id, age_from, age_to, sex, offset)
        return recieved_profiles

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
        return result

    def city_name_to_id(self, city_name):
        try:
            print('Перевод названия города в id')
            city_id = self.ext_get_api.database.getCities(country_id=1, q=city_name)["items"][0]["id"]
            return city_id
        except KeyError:
            print('Ошибка перевода названия города в id')
            return