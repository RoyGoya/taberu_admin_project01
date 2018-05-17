# Larger Applications
# http://flask.pocoo.org/docs/0.12/patterns/packages/


from flask import Flask

from flask_login import LoginManager, login_required

from .database import db_session
from .views.index_views import IndexView
# from .views.users_view import RegisterView, ProfileView, LoginView, LogoutView
from .views.tag_views import TagListView, TagDetailView
from .views.nutrition_views import NutritionView, DetailNutritionView, \
    CreateNutritionView
# from .models.users_model import User
from .apis.nutrition_apis import NutritionList, NTPattern2List


app = Flask(__name__)

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


# Decorate Views
# http://flask.pocoo.org/docs/0.12/views/
# index_view = login_required(IndexView.as_view(
#     'index_page', template_name='index.html'
# ))
# register_view = RegisterView.as_view(
#     'register_page', template_name='users/register.html'
# )
# login_view = LoginView.as_view(
#     'login_page', template_name='users/login.html'
# )
# logout_view = login_required(LogoutView.as_view(
#     'logout_action', next_url='index_page'
# ))
# profile_view = login_required(ProfileView.as_view(
#     'profile_page', template_name='users/profile.html'
# ))
list_tag_view = TagListView.as_view(
    'list_tag_page', template_name='tags/list_tag.html'
)
detail_tag_view = TagDetailView.as_view(
    'detail_tag_page', template_name='tags/detail_tag.html'
)
nutrition_view = NutritionView.as_view(
    'nutrition_page', template_name='nutrition.html'
)

nutritionlist_api_view = NutritionList.as_view('nutritionlist_api')
ntpattern2_api_view = NTPattern2List.as_view('ntpattern2_api')


# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/
# app.add_url_rule('/', view_func=index_view)
# app.add_url_rule('/register', view_func=register_view)
# app.add_url_rule('/login', view_func=login_view)
# app.add_url_rule('/logout', view_func=logout_view)
# app.add_url_rule('/profile', view_func=profile_view)
app.add_url_rule('/tags', view_func=list_tag_view)
app.add_url_rule('/tags/detail', view_func=detail_tag_view)
app.add_url_rule('/nutrition', view_func=nutrition_view)

app.add_url_rule('/api/nutrition/nutritionlist',
                 view_func=nutritionlist_api_view, methods=['GET'])
app.add_url_rule('/api/nutrition/getntpattern2/',
                 view_func=ntpattern2_api_view, methods=['GET'])


if __name__ == '__main__':
    app.run()
