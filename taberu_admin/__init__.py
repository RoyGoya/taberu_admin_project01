# Larger Applications
# http://flask.pocoo.org/docs/0.12/patterns/packages/


from flask import Flask

from flask_login import LoginManager, login_required

from .database import db_session
from .urls import url_patterns

# from .models.users_model import User


app = Flask('taberu_admin')

# Configuration Handling
# http://flask.pocoo.org/docs/0.12/config/
app.config.from_object('taberu_admin.config.DevelopmentConfig')
app.config.from_pyfile('settings.cfg')
# app.config.from_envvar('TABERU_ADMIN_SETTINGS')

# Flask-Login
# https://flask-login.readthedocs.io/en/latest/
# login_manager = LoginManager()
# login_manager.login_view = "login_page"
# login_manager.login_message = u"Please log in to access this page."
# login_manager.init_app(app)


# Flask-Login
# https://flask-login.readthedocs.io/en/latest/
# @login_manager.user_loader
# def load_user(user_email):
#     user = User.query.filter_by(email=user_email).first()
#     return user


# SQLAlchemy
# http://flask-sqlalchemy.pocoo.org/2.3/
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


for pattern in url_patterns:
    pattern_len = len(pattern)
    if pattern_len > 2:
        app.add_url_rule(pattern[0], view_func=pattern[1], methods=pattern[2])
    else:
        app.add_url_rule(pattern[0], view_func=pattern[1])
