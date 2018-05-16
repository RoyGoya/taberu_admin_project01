
from flask import request, jsonify
from flask.views import MethodView

from ..models.nutrition_models import Nutrition, NutritionPattern


class NutritionList(MethodView):

    def get(self):
        dt_pattern = request.args.get('dtPattern')
        nt_pattern1 = request.args.get('ntPattern1')
        if dt_pattern is None:
            pass
        else:
            dict_data = dict()
            nutrition_list = Nutrition.query.filter(
                Nutrition.dt_pattern==dt_pattern,
                Nutrition.nt_pattern1==nt_pattern1,
                Nutrition.is_active==True
            ).all()
            for nutrition in nutrition_list:
                names = []
                names.append(nutrition.dt_pattern)
                names.append(nutrition.nt_pattern1)
                names.append(nutrition.nt_pattern2)
                names.append(nutrition.eng_name)
                label_name = ''.join(names)
                dict_data[label_name] = label_name
            json_data = jsonify(dict_data)
            return json_data


class NTPattern2List(MethodView):

    def get(self):
        nt_pattern1 = request.args.get('ntPattern1')
        if nt_pattern1 is None:
            pass
        else:
            dict_data = dict()
            nutrition_patterns = NutritionPattern.query.filter(
                NutritionPattern.pattern1==nt_pattern1,
                NutritionPattern.pattern2!='00',
                NutritionPattern.is_active==True
            ).all()
            for n_pattern in nutrition_patterns:
                dict_data[n_pattern.eng_name] = n_pattern.pattern2
            json_data = jsonify(dict_data)
            return json_data
