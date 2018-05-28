
from .views.index_views import IndexView
# from .views.users_view import RegisterView, ProfileView, LoginView, LogoutView
from .views.tag_views import TagListView, TagDetailView
from .views.nutrient_views import NutritionView
from .apis.nutrient_apis import NutrientAPI, NutrientPattern2API, \
    FactorSetAPI, FactorAPI, NutrientFormAPI

# Decorate Views
# http://flask.pocoo.org/docs/0.12/views/
# index_view = login_required(IndexView.as_view(
#     'index_page', template_name='index.html'
# ))
index_view = IndexView.as_view(
    '/', template_name='index.html'
)
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
nutrient_view = NutritionView.as_view(
    'nutrition_page', template_name='nutrient/base_nutrient.html'
)

nutrient_api = NutrientAPI.as_view(
    'nutrient_api', template='nutrient/list_nutrient.html')
nutrient_form_api = NutrientFormAPI.as_view(
    'nutrient_form_api', template='nutrient/detail_nutrient.html')
nutrient_pattern2_api = NutrientPattern2API.as_view(
    'nutrient_pattern2_api', template='nutrient/inputs_nutrient.html')
factor_set_api = FactorSetAPI.as_view(
    'factor_set_api', template='nutrient/detail_factor.html')
factor_api = FactorAPI.as_view(
    'factor_api', templates={'initial': 'nutrient/list_factor.html',
                             'table': 'nutrient/table_factor.html',
                             'opted': 'nutrient/opted_factor.html'})

# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/
# app.add_url_rule('/', view_func=index_view)
# app.add_url_rule('/register', view_func=register_view)
# app.add_url_rule('/login', view_func=login_view)
# app.add_url_rule('/logout', view_func=logout_view)
# app.add_url_rule('/profile', view_func=profile_view)
# app.add_url_rule('/tags', view_func=list_tag_view)
# app.add_url_rule('/tags/detail', view_func=detail_tag_view)

url_patterns = [
    ('/', index_view),
    ('/nutrient', nutrient_view),
    ('/api/nutrients', nutrient_api, ['GET'], {'nutrient_code': None}),
    ('/api/nutrients/<string:nutrient_code>', nutrient_api, ['GET']),
    ('/api/nutrient-form', nutrient_form_api, ['GET']),
    ('/api/nutrient-pattern2', nutrient_pattern2_api, ['GET']),
    ('/api/factor-set/<string:nutrient_code>', factor_set_api, ['GET']),
    ('/api/factors', factor_api, ['GET'], {'factor_code': None}),
    ('/api/factors/<string:factor_code>', factor_api, ['GET']),
    ('/api/factors/create', factor_api, ['POST'])
]
