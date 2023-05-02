import sqlalchemy as sq
from sqlalchemy import orm
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from config import db_url_object


# Создание таблиц
metadata = MetaData()
Base = declarative_base()

engine = create_engine(db_url_object)
Session = sessionmaker(bind=engine)

session = Session()
connection = engine.connect()

# Таблица просмотренных анкет
class Viewed(Base):
    __tablename__ = 'viewed'

    profile_id = sq.Column(sq.Integer, primary_key=True)  # Профиль пользователя
    worksheet_id = sq.Column(sq.Integer, primary_key=True)  # ID просмотренной анкеты


# engine = create_engine(db_url_object, echo = True)  # echo = True - для того, чтобы в консоли отображались логи операций с БД
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

# Функции для работы с БД

def create_all():  # Создание таблицы
    Base.metadata.create_all(engine)


def add_viewed(profile_id, worksheet_id):  # Добавление записи в БД
    try:
        to_db = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_db)
    except (IntegrityError, InvalidRequestError):
        return False
    return True


def check_viewed(profile_id, worksheet_id):  # Извлечение записей из БД
    #from_db = session.query(Viewed).filter(Viewed.profile_id == profile_id).all()
    viewed_user = session.query(Viewed).filter(Viewed.profile_id == profile_id, Viewed.worksheet_id == worksheet_id).first()
    return bool(viewed_user)

