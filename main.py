"""Модуль запуска бота VKinder
"""
from interface import BotInterface
from config import access_token, community_token, access_token


if __name__ == '__main__':
    bot = BotInterface(community_token)
    bot.handler()
