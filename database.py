"""Модуль работы с Базой данных
"""
import sqlalchemy as sq
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from config import db_url_object


metadata = MetaData()
Base = declarative_base()

engine = create_engine(db_url_object)
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()


"""Таблица просмотренных анкет
"""


class Viewed(Base):
    __tablename__ = 'viewed'

    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)


def create_all():
    Base.metadata.create_all(engine)
    print('Создание таблицы')


def wipe_all():
    Base.metadata.drop_all(engine)
    create_all()
    print('Таблица очищена')


def add_viewed(profile_id, worksheet_id):
    try:
        to_db = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_db)
        session.commit()
    except (IntegrityError, InvalidRequestError):
        return False
    print('Профиль добавлен в Базу данных')
    return True


def check_viewed(profile_id, worksheet_id):
    from_db = session.query(Viewed).filter(Viewed.profile_id == profile_id).all()
    worksheets_list = [worksheet.worksheet_id for worksheet in from_db]
    if worksheet_id in worksheets_list:
        print('Пользователь уже в Базе данных')
        return True
    else:
        print('Это новый для пользователя профиль')
        return False
