import sqlalchemy as sq
from sqlalchemy import create_engine, MetaData, exists, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from config import db_url_object


# Создание таблиц
metadata = MetaData()  # Функция для управления таблицами
Base = declarative_base()  # Для того чтобы класс Viewed был унаследован от базовой модели

# Создание движка алхимии и сессии
engine = create_engine(db_url_object)  # Создаем движок, для работы с БД
Session = sessionmaker(bind=engine)  # Используем класс sessionmaker для простоты вызова класса Session
session = Session()  # Объект session на основе класса Session, созданного sessionmaker'ом для всех взаимодействий с БД
connection = engine.connect()  # Метод для управления подключением к БД


# Таблица просмотренных анкет
class Viewed(Base):
    __tablename__ = 'viewed'  # Название таблицы

    profile_id = sq.Column(sq.Integer, primary_key=True)  # ID пользователя
    worksheet_id = sq.Column(sq.Integer, primary_key=True)  # ID просмотренной анкеты

# Функции для работы с БД
def create_all():  # Создание таблиц, в моем случае одной
    Base.metadata.create_all(engine)  # Используется метод create_all()
    print('Создание таблицы')


def wipe_all():  # Ликвидация таблицы
    Base.metadata.drop_all(engine)  # Используется метод drop_all()
    print('Таблица ликвидирована')


def add_viewed(profile_id, worksheet_id):  # Добавление записи в БД
    try:
        to_db = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_db)
        session.commit()  # Коммит для подтверждения транзакции
    except (IntegrityError, InvalidRequestError):
        return False
    print('Профиль добавлен в Базу данных')
    return True


def check_viewed(profile_id, worksheet_id):  # Проверка просмотрена ли анкета
    from_db = session.query(Viewed).filter(Viewed.profile_id == profile_id).all()
    worksheets_list = [worksheet.worksheet_id for worksheet in from_db]  # Итерация по просмотренным анкетам, записываем их в список
    if worksheet_id in worksheets_list:  # Проверяем есть ли новая анкета в списке просмотренных
        print('Пользователь уже в Базе данных')
        return True
    else:
        print('Это новый для пользователя профиль')
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
