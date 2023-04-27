import sqlalchemy as sq
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config import db_url_object


# Создание таблиц

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    viewed = relationship('Viewed', secondary='user_to_viewed')


class Viewed(Base):
    __tablename__ = 'viewed'

    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    screen_name = sq.Column(sq.String)
    photos = relationship('Photo', backref='viewed')
    users = relationship('User', secondary='user_to_viewed')


class Photo(Base):
    __tablename__ = 'photo'

    id = sq.Column(sq.String, primary_key=True)
    photo_id = sq.Column(sq.Integer)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('viewed.id'))
    likes_count = sq.Column(sq.Integer)
    comments_count = sq.Column(sq.Integer)


user_to_viewed = sq.Table(
    'user_to_viewed',
    Base.metadata,
    sq.Column('user_id', sq.Integer, sq.ForeignKey('user_id')),
    sq.Column('viewed_id', sq.Integer, sq.ForeignKey('viewed_id'))
)


engine = sq.create_engine(db_url_object, echo = True)
# echo = True - для того, чтобы в консоли отображались логи операций с БД
Base.metadata.create_all(engine)
Session = orm.sessionmaker(bind=engine)


class DBTools():

    def __init__(self, ):

# Добавление записи в БД

engine = sq.create_engine(db_url_object)
Session = orm.sessionmaker(bind=engine)
session = Session()
to_db = Viewed(profile_id=123, worksheet_id=3221)
session.add(to_db)


# Извлечение записей из БД

engine = sq.create_engine(db_url_object)
Session = orm.sessionmaker()
session = Session()
session.commit()
from_db = session.query(Viewed).filter(Viewed.profile_id==123).all()


