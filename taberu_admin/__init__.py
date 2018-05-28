# Larger Applications
# http://flask.pocoo.org/docs/0.12/patterns/packages/


from flask import Flask

from flask_login import LoginManager, login_required
from raven.contrib.flask import Sentry

from .database import db_session
from .urls import url_patterns
from .errors import InvalidUsage, handle_invalid_usage
# from .models.users_model import User


app = Flask('taberu_admin')

# Configuration Handling
# http://flask.pocoo.org/docs/0.12/config/
app.config.from_object('taberu_admin.config.DevelopmentConfig')
app.config.from_pyfile('settings.cfg')
# app.config.from_envvar('TABERU_ADMIN_SETTINGS')

# Set-up Raven Sentry
sentry = Sentry(app, dsn='https://42db0d82433d4346b828266f9f1961d8:263209988e554541b91c79fefbfb0904@sentry.io/1214614')

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


# Set-up URLs
for pattern in url_patterns:
    pattern_len = len(pattern)
    if pattern_len == 2:
        app.add_url_rule(pattern[0], view_func=pattern[1])
    elif pattern_len == 3:
        app.add_url_rule(pattern[0], view_func=pattern[1], methods=pattern[2])
    else:
        app.add_url_rule(pattern[0], view_func=pattern[1], methods=pattern[2],
                         defaults=pattern[3])

# Register Error handlers
app.register_error_handler(InvalidUsage, handle_invalid_usage)
