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


# engine = create_engine(db_url_object, echo = True)  # echo = True - для того, чтобы в консоли отображались логи операций с БД
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

# Функции для работы с БД

def create_all():  # Создание таблицы
    Base.metadata.create_all(engine)


def wipe_all():  # Ликвидация таблицы
    Base.metadata.drop_all(engine)


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
    from_db = session.query(Viewed).filter(Viewed.profile_id == profile_id).all()
    worksheets_list = [worksheet.worksheet_id for worksheet in from_db]
    if worksheet_id in worksheets_list:
        print('true')
        return True
    else:
        print('false')
        return False


if __name__ == '__main__':
    create_all()

    # Проверка создания записи просмотренной анкеты
    # add_viewed(111, 222)

    # Проверка просмотрена ли анкета
    # check_viewed(123, 321)

    # # Проверка вытаскивания просмотренных в список
    # q = query_viewed(123)
    # q

    # Проверка на наличие и занесение в БД
    # users_record = session.query(Viewed).filter_by(profile_id='123').scalar()
    # if not users_record:
    #     users_record = User_search_data(id=item['id'])
    # session.add(users_record)
    # session.commit()

    # Тестирую код для проверки просмотра анкеты
    # worksheet_id = 321
    # rows = session.query(Viewed).filter(Viewed.profile_id == '123').all()
    # values = [row.worksheet_id for row in rows]
    # print(values)
    # if worksheet_id in values:
    #     print('true')
    # else:
    #     print('false')

    # Проверка функции проверка просмотра анкеты
    # check_viewed(123, 321)
