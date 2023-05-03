import sqlalchemy as sq
import psycopg2
from sqlalchemy import orm
from sqlalchemy import create_engine, MetaData, exists, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
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


# Функции для работы с БД
def create_all():  # Создание таблицы
    Base.metadata.create_all(engine)


def add_viewed(profile_id, worksheet_id):  # Добавление записи в БД
    try:
        to_db = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_db)
        session.commit()
    except (IntegrityError, InvalidRequestError):
        return False
    return True


def query_viewed(profile_id):
    from_db = session.query(Viewed).filter(Viewed.profile_id == profile_id).all()
    print(from_db)
    return from_db


def check_viewed(profile_id, worksheet_id):  # Проверка просмотрена ли анкета
    check_exists = session.query(exists().where(Viewed.profile_id == profile_id, Viewed.worksheet_id == worksheet_id)).scalar()
    print(check_exists)


if __name__ == '__main__':
    # create_all()

    # Проверка создания записи просмотренной анкеты
    # add_viewed(123, 321)

    # Проверка просмотрена ли анкета
    # check_viewed(123, 321)

    # Проверка вытаскивания просмотренных в список
    # q = query_viewed(123)
    # q

    # all = sq.select([Viewed])
    # all_result = connection.execute(all)
    # print(all_result.fetchall())
