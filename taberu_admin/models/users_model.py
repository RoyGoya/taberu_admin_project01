# SQLAlchemy
# http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/
# flask_user_sign_in.html


from sqlalchemy import Column, Integer, VARCHAR, Boolean, DATETIME
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from taberu_admin.database import Base
from taberu_admin.helpers.timezone_gen import utc_now


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(255), unique=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(VARCHAR(30))
    last_name = Column(VARCHAR(30))
    created_datetime = Column(DATETIME)
    password_hash = Column(VARCHAR(100))

    def __init__(self, email=None, password=None, first_name=None,
                 last_name=None, is_active=True,
                 created_datetime=utc_now().isoformat()):
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.created_datetime = created_datetime

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
