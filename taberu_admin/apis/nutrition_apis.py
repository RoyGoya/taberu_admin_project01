
from flask import request, Response, jsonify, render_template
from flask.views import MethodView

from ..forms.nutrition_forms import CreateNutritionForm, get_nt_pattern2_choices
from ..models.nutrition_models import Nutrition, NutritionPattern


class NutritionList(MethodView):

    def get(self):
        dt_pattern = request.args.get('dtPattern')
        nt_pattern1 = request.args.get('ntPattern1')
        list_data = []
        if dt_pattern is None:
            pass
        elif nt_pattern1 is None:
            nutrition_list = Nutrition.query.filter(
                Nutrition.dt_pattern==dt_pattern,
                Nutrition.is_active==True
            ).all()
        else:
            nutrition_list = Nutrition.query.filter(
                Nutrition.dt_pattern==dt_pattern,
                Nutrition.nt_pattern1==nt_pattern1,
                Nutrition.is_active==True
            ).all()
        for index, nutrition in enumerate(nutrition_list):
            eng_name = nutrition.eng_name
            is_set = nutrition.is_set
            dt_pattern = nutrition.dt_pattern
            nt_pattern1 = nutrition.nt_pattern1
            nt_pattern2 = nutrition.nt_pattern2
            serial = nutrition.serial
            list_data.append(
                {
                    'dt_pattern': dt_pattern,
                    'nt_pattern1': nt_pattern1,
                    'nt_pattern2': nt_pattern2,
                    'serial': serial,
                    'eng_name': eng_name,
                    'is_set': is_set
                }
            )

        list_cnt = len(list_data)
        list_data.insert(0, {'cnt': list_cnt})
        test = jsonify(list_data)
        return test


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


class NutritionFormTemplate(MethodView):

    def get(self):
        request_args = request.args
        dt_pattern = request_args.get('dt_pattern')
        nt_pattern1 = request_args.get('nt_pattern1')
        nt_pattern2 = request_args.get('nt_pattern2')
        serial = request_args.get('serial')

        nutrition = Nutrition.query.filter(
            Nutrition.dt_pattern==dt_pattern,
            Nutrition.nt_pattern1==nt_pattern1,
            Nutrition.nt_pattern2==nt_pattern2,
            Nutrition.serial==serial
        ).first()
        nt_pattern2_choices = get_nt_pattern2_choices(nt_pattern1)
        form = CreateNutritionForm(request.form)
        form.nt_pattern2.choices = nt_pattern2_choices

        form.dt_pattern.data = nutrition.dt_pattern
        form.nt_pattern1.data = nutrition.nt_pattern1
        form.nt_pattern2.data = nutrition.nt_pattern2
        form.is_set.data = str(nutrition.is_set)
        form.is_active.data = str(nutrition.is_active)
        form.eng_name.data = nutrition.eng_name
        form.eng_plural.data = nutrition.eng_plural
        form.kor_name.data = nutrition.kor_name
        form.jpn_name.data = nutrition.jpn_name
        form.chn_name.data = nutrition.chn_name
        return render_template('nutrition/nt_form.html', form=form,
                               nutrition=nutrition)
