# SQLAlchemy
# http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/
# flask-login
# https://code.tutsplus.com/tutorials/intro-to-flask-signing-in-and-out--net-29982


from sqlalchemy import Column, Integer, VARCHAR, Boolean, DATETIME
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from taberu_admin.database import Base
from taberu_admin.helpers.timezone_gen import get_utc_datetime


class User(Base, UserMixin):
    __tablename__ = 'admin_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(255), unique=True)
    is_active = Column(Boolean, default=True)
    last_login_datetime = Column(DATETIME)
    created_datetime = Column(DATETIME)
    password_hash = Column(VARCHAR(100))
    first_name = Column(VARCHAR(100))
    last_name = Column(VARCHAR(100))

    def __init__(self, email=None, is_active=True,
                 last_login_datetime=get_utc_datetime().isoformat(),
                 created_datetime=get_utc_datetime().isoformat(),
                 password=None, first_name=None, last_name=None):
        self.email = email
        self.is_active = is_active
        self.last_login_datetime = last_login_datetime
        self.created_datetime = created_datetime
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User %r>' % (self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        # This custom method's used by @login_manager.user_loader
        try:
            return self.email
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


class AdminUser(Base):
    __tablename__ = 'admin_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    is_active = Column(Boolean)
    is_authenticated = Column(Boolean)
    access_level = Column(VARCHAR(6))
    eng_name = Column(VARCHAR(100))

    def __init__(self, user_id=None, is_active=None,
                 is_authenticated=None, access_level=None, eng_name=None):
        self.user_id = user_id
        self.is_active = is_active
        self.is_authenticated = is_authenticated
        self.access_level = access_level
        self.eng_name = eng_name

    def __repr__(self):
        return '<AdminUser %r>' % (self.user_id)
