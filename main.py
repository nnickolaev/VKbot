"""Модуль запуска бота VKinder
"""
from interface import BotInterface
from config import access_token, community_token, access_token


if __name__ == '__main__':
    try:
        bot = BotInterface(community_token)
        bot.handler()
    except KeyError:
        print(KeyError)