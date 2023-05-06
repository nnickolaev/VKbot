"""Модуль запуска бота VKinder
"""
import vk_api
from config import access_token
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import sqlalchemy as sq
from sqlalchemy import orm
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import db_url_object
from core import VkTools
from database import engine, Viewed
from interface import BotInterface
from config import community_token

if __name__ == '__main__':
    # try:
    #     bot = BotInterface(community_token)
    #     bot.handler()
    # except KeyError:
    #     print(KeyError)
