from .views import IndexView, NutrientView
from .apis.nutrient_apis import NutrientAPI, NutrientPatternAPI, \
    NutrientFormAPI, NutrientSetAPI, NutrientOptionFormAPI
from .apis.factor_apis import FactorAPI, FactorSetAPI


class UrlMapper:
    def __init__(self, app):
        self.app = app

    def set_urls(self):
        index_view = IndexView.as_view(
            name='index_page',
            template='base_index.html'
        )
        nutrient_view = NutrientView.as_view(
            name='nutrient_page',
            template='base_nutrient.html'
        )
        nutrient_api = NutrientAPI.as_view(
            name='nutrient_api',
            templates={'list': 'nutrients/box_list_nutrient.html',
                       'get': 'nutrients/box_get_nutrient.html',
                       'table': 'nutrients/table_nutrient.html',
                       'opted': 'nutrients/opted_nutrient.html',
                       'detail': 'nutrients/box_detail_nutrient.html'}
        )
        nutrient_set_api = NutrientSetAPI.as_view(
            name='nutrient_set_api',
            templates={'sub': 'nutrients/box_sub_nutrient.html',
                       'opted': 'nutrients/opted_nutrient.html'}
        )
        nutrient_form_api = NutrientFormAPI.as_view(
            name='nutrient_form_api',
            template='nutrients/box_detail_nutrient.html'
        )
        nutrient_pattern2_api = NutrientPatternAPI.as_view(
            name='nutrient_pattern2_api',
            template='nutrients/inputs_nutrient.html'
        )
        nutrient_option_form_api = NutrientOptionFormAPI.as_view(
            name='nutrient_option_api',
            templates={'option': 'nutrients/option_nutrient.html',
                       'pattern2': 'nutrients/option_pattern2_nutrient.html'}
        )
        factor_api = FactorAPI.as_view(
            name='factor_api',
            templates={'list': 'factors/box_list_factor.html',
                       'table': 'factors/table_factor.html',
                       'opted': 'factors/opted_factor.html'}
        )
        factor_set_api = FactorSetAPI.as_view(
            name='factor_set_api',
            templates={'detail': 'factors/box_detail_factor.html',
                       'opted': 'factors/opted_factor.html'}
        )
        self.app.add_url_rule(
            rule='/',
            methods=['GET', 'POST'],
            view_func=index_view
        )
        self.app.add_url_rule(
            rule='/nutrients',
            methods=['GET', 'POST'],
            view_func=nutrient_view
        )
        self.app.add_url_rule(
            rule='/api/nutrients',
            view_func=nutrient_api,
            methods=['GET'],
            defaults={'nutrient_code': None}
        )
        self.app.add_url_rule(
            rule='/api/nutrients',
            view_func=nutrient_api,
            methods=['POST']
        )
        self.app.add_url_rule(
            rule='/api/nutrients/<string:nutrient_code>',
            view_func=nutrient_api,
            methods=['GET', 'PUT', 'DELETE']
        )
        self.app.add_url_rule(
            rule='/api/nutrient-set',
            view_func=nutrient_set_api,
            methods=['GET'],
            defaults={'nutrient_set_code': None}
        )
        self.app.add_url_rule(
            rule='/api/nutrient-set',
            view_func=nutrient_set_api,
            methods=['POST']
        )
        self.app.add_url_rule(
            rule='/api/nutrient-set/<string:nutrient_set_code>',
            view_func=nutrient_set_api,
            methods=['GET', 'PUT', 'DELETE']
        )
        self.app.add_url_rule(
            rule='/api/nutrient-form',
            view_func=nutrient_form_api,
            methods=['GET'],
            defaults={'nutrient_code': None}
        )
        self.app.add_url_rule(
            rule='/api/nutrient-form/<string:nutrient_code>',
            view_func=nutrient_form_api,
            methods=['GET']
        )
        self.app.add_url_rule(
            rule='/api/nutrient-pattern2/<string:pattern1_code>',
            view_func=nutrient_pattern2_api,
            methods=['GET']
        )
        self.app.add_url_rule(
            rule='/api/nutrient-option',
            view_func=nutrient_option_form_api,
            methods=['GET'],
            defaults={'pattern1_code': None}
        )
        self.app.add_url_rule(
            rule='/api/nutrient-option/<string:pattern1_code>',
            view_func=nutrient_option_form_api,
            methods=['GET']
        )
        self.app.add_url_rule(
            rule='/api/factor-set',
            view_func=factor_set_api,
            methods=['GET'],
            defaults={'factor_set_code': None}
        )
        self.app.add_url_rule(
            rule='/api/factor-set/<string:factor_set_code>',
            view_func=factor_set_api,
            methods=['GET', 'PUT', 'DELETE']
        )
        self.app.add_url_rule(
            rule='/api/factor-set',
            view_func=factor_set_api,
            methods=['POST']
        )
        self.app.add_url_rule(
            rule='/api/factors',
            view_func=factor_api,
            methods=['GET'],
            defaults={'factor_code': None}
        )
        self.app.add_url_rule(
            rule='/api/factors/<string:factor_code>',
            view_func=factor_api,
            methods=['GET']
        )
