
from .views.index_views import IndexView
# from .views.users_view import RegisterView, ProfileView, LoginView, LogoutView
from .views.tag_views import TagListView, TagDetailView
from .views.nutrition_views import NutritionView, DetailNutritionView, \
    CreateNutritionView
from .apis.nutrition_apis import NutritionListTemplate, NutritionPattern2, \
    NutritionDetailTemplate, NutritionFactorDetail, NutritionFactorList

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
nutrition_view = NutritionView.as_view(
    'nutrition_page', template_name='nutrition/base_nt.html'
)

nutrition_nlist_api = NutritionListTemplate.as_view(
    'nutrition_list_api')
nutrition_pattern2_api = NutritionPattern2.as_view(
    'nutrition_pattern2_api')
nutrition_ndetail_api = NutritionDetailTemplate.as_view(
    'nutrition_detail_api')
nutrition_fdetail_api = NutritionFactorDetail.as_view(
    'nutrition_factor_detail_api')
nutrition_flist_api = NutritionFactorList.as_view(
    'nutrition_factor_list_api'
)

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
    ('/nutrition', nutrition_view),
    ('/api/nutrition/list', nutrition_nlist_api, ['GET']),
    ('/api/nutrition/detail', nutrition_ndetail_api, ['GET']),
    ('/api/nutrition/pattern2', nutrition_pattern2_api, ['GET']),
    ('/api/nutrition/factor/list', nutrition_flist_api, ['GET']),
    ('/api/nutrition/factor/detail', nutrition_fdetail_api, ['GET'])
]
