
from flask import request, Response, jsonify, render_template
from flask.views import MethodView

from sqlalchemy import and_

from ..database import Base
from ..forms.nutrition_forms import CreateNutritionForm, \
    get_nutrition_pattern2_choices
from ..models.nutrition_models import Nutrition, NutritionPattern,\
    NutritionFactorSet, NutritionFactor


class NutritionListTemplate(MethodView):

    def get(self):
        dt_pattern = request.args.get('dt_pattern')
        pattern1 = request.args.get('pattern1')
        list_data = []
        if dt_pattern is None:
            pass
        elif pattern1 is None:
            nutrition_list = Nutrition.query.filter(
                Nutrition.dt_pattern==dt_pattern,
                Nutrition.is_active==True
            ).all()
        else:
            nutrition_list = Nutrition.query.filter(
                Nutrition.dt_pattern==dt_pattern,
                Nutrition.pattern1==pattern1,
                Nutrition.is_active==True
            ).all()
        nutrition_list_len = len(list_data)
        return render_template('nutrition/list_nt.html',
                               nutrition_list=nutrition_list,
                               nutrition_list_cnt=nutrition_list_len)


class NutritionPattern2(MethodView):

    def get(self):
        npattern1 = request.args.get('pattern1')
        if npattern1 is None:
            pass
        else:
            dict_data = dict()
            nutrition_patterns = NutritionPattern.query.filter(
                NutritionPattern.pattern1==npattern1,
                NutritionPattern.pattern2!='00',
                NutritionPattern.is_active==True
            ).all()
            for n_pattern in nutrition_patterns:
                dict_data[n_pattern.eng_name] = n_pattern.pattern2
            json_data = jsonify(dict_data)
            return json_data


class NutritionDetailTemplate(MethodView):

    def get(self):
        requests = request.args
        dt_pattern = requests.get('dt_pattern')
        pattern1 = requests.get('pattern1')
        pattern2 = requests.get('pattern2')
        serial = requests.get('serial')

        nutrition = Nutrition.query.filter(
            Nutrition.dt_pattern == dt_pattern,
            Nutrition.pattern1 == pattern1,
            Nutrition.pattern2 == pattern2,
            Nutrition.serial == serial
        ).first()
        pattern2_choices = get_nutrition_pattern2_choices(pattern1)
        form = CreateNutritionForm(request.form)
        form.pattern2.choices = pattern2_choices

        form.dt_pattern.data = nutrition.dt_pattern
        form.pattern1.data = nutrition.pattern1
        form.pattern2.data = nutrition.pattern2
        form.has_sub.data = str(nutrition.has_sub)
        form.is_active.data = str(nutrition.is_active)
        form.eng_name.data = nutrition.eng_name
        form.eng_plural.data = nutrition.eng_plural
        form.kor_name.data = nutrition.kor_name
        form.jpn_name.data = nutrition.jpn_name
        form.chn_name.data = nutrition.chn_name
        return render_template('nutrition/detail_nt.html', form=form,
                               nutrition=nutrition)


class NutritionFactorDetail(MethodView):

    def get(self):
        requests = request.args
        dt_pattern = requests.get('dt_pattern')
        pattern1 = requests.get('pattern1')
        pattern2 = requests.get('pattern2')
        serial = requests.get('serial')

        # Get Selected Nutrition's Factors
        fset_suq = NutritionFactorSet.query.filter(
            NutritionFactorSet.nutrition_dt_pattern==dt_pattern,
            NutritionFactorSet.nutrition_pattern1==pattern1,
            NutritionFactorSet.nutrition_pattern2==pattern2,
            NutritionFactorSet.nutrition_serial==serial
        ).subquery()
        factors = NutritionFactor.query.join(fset_suq, and_(
                fset_suq.c.nf_pattern1==NutritionFactor.pattern1,
                fset_suq.c.nf_pattern2==NutritionFactor.pattern2,
                fset_suq.c.nf_pattern3==NutritionFactor.pattern3,
                fset_suq.c.nf_pattern4==NutritionFactor.pattern4
            )).all()

        # Get Selected Nutrition Info
        nutrition = Nutrition.query.filter(
            Nutrition.dt_pattern == dt_pattern,
            Nutrition.pattern1 == pattern1,
            Nutrition.pattern2 == pattern2,
            Nutrition.serial == serial
        ).first()
        factors_len = len(factors)
        return render_template('nutrition/factor_detail_nt.html',
                               factors=factors, factors_cnt=factors_len,
                               nutrition=nutrition)


class NutritionFactorList(MethodView):

    def get(self):
        requests = request.args
        pattern1 = requests.get('pattern1')
        pattern2 = requests.get('pattern2')
        pattern3 = requests.get('pattern3')
        pattern4 = requests.get('pattern4')

        if pattern1 is None:
            factors = NutritionFactor.query.filter(
                NutritionFactor.pattern2=='0'
            ).all()
        elif pattern2 is None:
            factors = NutritionFactor.query.filter(
                NutritionFactor.pattern1==pattern1,
            ).all()
        elif pattern3 is None:
            factors = NutritionFactor.query.filter(
                NutritionFactor.pattern1==pattern1,
                NutritionFactor.pattern2==pattern2
            ).all()
        elif pattern4 is None:
            factors = NutritionFactor.query.filter(
                NutritionFactor.pattern1==pattern1,
                NutritionFactor.pattern2==pattern2,
                NutritionFactor.pattern3==pattern3
            ).all()
        else:
            factors = NutritionFactor.query.filter(
                NutritionFactor.pattern1==pattern1,
                NutritionFactor.pattern2==pattern2,
                NutritionFactor.pattern3==pattern3,
                NutritionFactor.pattern4==pattern4
            ).all()
        factors_len = len(factors)
        return render_template('nutrition/factor_list_nt.html',
                               factors=factors, factors_cnt=factors_len)
