from flask import request, Response, jsonify, render_template
from flask.views import MethodView

from sqlalchemy import and_

from ..database import Base
from ..forms.nutrient_forms import CreateNutrientForm, \
    get_nutrient_pattern2_choices
from ..models.nutrient_models import Nutrient, NutrientPattern,\
    FactorSet, Factor


class NutrientListTemplate(MethodView):

    def get(self) -> object:
        dt_pattern = request.args.get('dt_pattern')
        pattern1 = request.args.get('pattern1')
        list_data = []
        if dt_pattern is None:
            pass
        elif pattern1 is None:
            nutrient_list = Nutrient.query.filter(
                Nutrient.dt_pattern == dt_pattern,
                Nutrient.is_active == True
            ).all()
        else:
            nutrient_list = Nutrient.query.filter(
                Nutrient.dt_pattern == dt_pattern,
                Nutrient.pattern1 == pattern1,
                Nutrient.is_active == True
            ).all()
        nutrient_list_len = len(list_data)
        return render_template('nutrient/nutrient_list.html',
                               nutrients=nutrient_list,
                               nutrients_cnt=nutrient_list_len)


class NutrientPattern2(MethodView):

    def get(self) -> object:
        npattern1 = request.args.get('pattern1')
        if npattern1 is None:
            pass
        else:
            dict_data = dict()
            nutrient_patterns = NutrientPattern.query.filter(
                NutrientPattern.pattern1 == npattern1,
                NutrientPattern.pattern2 != '00',
                NutrientPattern.is_active == True
            ).all()
            for n_pattern in nutrient_patterns:
                dict_data[n_pattern.eng_name] = n_pattern.pattern2
            json_data = jsonify(dict_data)
            return json_data


class NutrientDetailTemplate(MethodView):

    def get(self) -> object:
        requests = request.args
        dt_pattern = requests.get('dt_pattern')
        pattern1 = requests.get('pattern1')
        pattern2 = requests.get('pattern2')
        serial = requests.get('serial')

        nutrient = Nutrient.query.filter(
            Nutrient.dt_pattern == dt_pattern,
            Nutrient.pattern1 == pattern1,
            Nutrient.pattern2 == pattern2,
            Nutrient.serial == serial
        ).first()
        pattern2_choices = get_nutrient_pattern2_choices(pattern1)
        form = CreateNutrientForm(request.form)
        form.pattern2.choices = pattern2_choices

        form.dt_pattern.data = nutrient.dt_pattern
        form.pattern1.data = nutrient.pattern1
        form.pattern2.data = nutrient.pattern2
        form.has_sub.data = str(nutrient.has_sub)
        form.is_active.data = str(nutrient.is_active)
        form.eng_name.data = nutrient.eng_name
        form.eng_plural.data = nutrient.eng_plural
        form.kor_name.data = nutrient.kor_name
        form.jpn_name.data = nutrient.jpn_name
        form.chn_name.data = nutrient.chn_name
        return render_template('nutrient/nutrient_detail.html', form=form,
                               nutrient=nutrient)


class NutrientFactorDetail(MethodView):

    def get(self) -> object:
        requests = request.args
        dt_pattern = requests.get('dt_pattern')
        pattern1 = requests.get('pattern1')
        pattern2 = requests.get('pattern2')
        serial = requests.get('serial')

        # Get Selected nutrient's Factors
        fset_suq = FactorSet.query.filter(
            FactorSet.nutrient_dt_pattern == dt_pattern,
            FactorSet.nutrient_pattern1 == pattern1,
            FactorSet.nutrient_pattern2 == pattern2,
            FactorSet.nutrient_serial == serial
        ).subquery()
        factors = Factor.query.join(fset_suq, and_(
            fset_suq.c.factor_pattern1 == Factor.pattern1,
            fset_suq.c.factor_pattern2 == Factor.pattern2,
            fset_suq.c.factor_pattern3 == Factor.pattern3,
            fset_suq.c.factor_pattern4 == Factor.pattern4
            )).all()

        # Get Selected nutrient Info
        nutrient = Nutrient.query.filter(
            Nutrient.dt_pattern == dt_pattern,
            Nutrient.pattern1 == pattern1,
            Nutrient.pattern2 == pattern2,
            Nutrient.serial == serial
        ).first()
        factors_len = len(factors)
        return render_template('nutrient/factor_detail.html',
                               factors=factors, factors_cnt=factors_len,
                               nutrient=nutrient)


class NutrientFactorList(MethodView):

    def get(self) -> object:
        requests = request.args
        factors = []
        template = ''
        request_type = requests.get('type')
        pattern1 = requests.get('pattern1')
        pattern2 = requests.get('pattern2')
        pattern3 = requests.get('pattern3')
        pattern4 = requests.get('pattern4')

        if request_type == 'addition':
            if pattern2 == '0':
                factors = Factor.query.filter(
                    Factor.pattern1 == pattern1,
                    Factor.pattern2 != '0',
                    Factor.pattern3 == '00',
                ).all()
            elif pattern3 == '00':
                factors = Factor.query.filter(
                    Factor.pattern1 == pattern1,
                    Factor.pattern2 == pattern2,
                    Factor.pattern3 != '00',
                    Factor.pattern4 == '00'
                ).all()
            elif pattern4 == '00':
                factors = Factor.query.filter(
                    Factor.pattern1 == pattern1,
                    Factor.pattern2 == pattern2,
                    Factor.pattern3 == pattern3,
                    Factor.pattern4 != '00'
                ).all()
            else:
                factors = Factor.query.filter(
                    Factor.pattern1 == pattern1,
                    Factor.pattern2 == pattern2,
                    Factor.pattern3 == pattern3,
                    Factor.pattern4 == pattern4
                ).all()
            template = 'nutrient/factor_list_part.html'
        elif request_type == 'initial':
            factors = Factor.query.filter(
                Factor.pattern2 == '0',
            ).all()
            template = 'nutrient/factor_list.html'

        factors_len = len(factors)
        return render_template(template, factors=factors,
                               factors_cnt=factors_len)
