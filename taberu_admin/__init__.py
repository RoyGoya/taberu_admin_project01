from flask import Flask

from raven.contrib.flask import Sentry

from .database import db_session
from .errors import InvalidUsage, handle_invalid_usage
from .urls import UrlMapper


app = Flask('taberu_admin')

# Configuration Handling
app.config.from_object('taberu_admin.config.DevelopmentConfig')
app.config.from_pyfile('settings.cfg')
# app.config.from_envvar('TABERU_ADMIN_SETTINGS')

# Set-up Raven Sentry
sentry = Sentry(app, dsn='https://42db0d82433d4346b828266f9f1961d8:263209988e554541b91c79fefbfb0904@sentry.io/1214614')


# SQLAlchemy
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Set URLs into Flask app.
urls = UrlMapper(app)
urls.set_urls()


# Register Error handlers
app.register_error_handler(InvalidUsage, handle_invalid_usage)
