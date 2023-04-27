import vk_api
from config import access_token
from vk_api.exceptions import ApiError


class VkTools():
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)

    # def get_profile_info(self, user_id):
    #
    #     try:
    #         info = self, vk_api.method('users.get',
    #                                    {'user_id': user_id,
    #                                     'fields': 'bday, city, sex, relation'
    #                                     }
    #                                    )
    #     except ApiError:
    #         return
    #
    #     return info

    def user_search(self, city_id, age_from, age_to, sex, offset = None):
        try:
            profiles = self.ext_api.method('user_search',
                                       {'city_id': 'city_id',
                                        'age_from': 'age_from',
                                        'age_to': 'age_to',
                                        'sex': 'sex',
                                        'count': 30,
                                        'offset': offset
                                        })

        except ApiError:
            return

        profiles = profiles['items'] # Чтобы фильтровать закрытые профили

        result = []
        for profile in profiles:
            if profile['is_closed'] == False:
                result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                               'id': profile['id']
                               })

        return result


    def photos_get(self, user_id):
        photos = self.ext_api.method('photos_get',
                                     {'album_id': 'profile',
                                      'owner_id': user_id
                                     }
                                     )
        try:
            photos = photos['items']
        except KeyError:
            return

        result = []
        for num, photo in enumerate(photos):
            result.append({'owner_id': photo['owner_id'],
                           'id': photo['id']
                           })
            if num == 2: # Чтобы выбирались три фотографии. Нужно еще допилить, чтобы выбирались 3 самые популярные
                break

        return result


if __name__ == '__main__':
    tools = VkTools(access_token)

    # info = tools.get_profile_info(789657038)
    # if info:
    #     print(tools.get_profile_info(789657038))
    # else:
    #     pass

    # profiles = tools.user_search(1, 20, 40, 1)
    # print(profiles)

    photos = tools.photos_get(709972842)
    print(photos)

    # вывод [{'owner_id': 709972942, 'id': 457239017}]

    media = f'photo_709972942_457239017'