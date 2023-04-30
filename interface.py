import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import access_token, community_token


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
        longpoll = VkLongPoll(self.bot)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                if request.lower() == 'привет':
                    self.message_send(event.user_id, 'Добрый день!')
                elif request.lower() == 'поиск':
                    pass
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

