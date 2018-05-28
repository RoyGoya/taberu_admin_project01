from flask import request, render_template
from flask.views import MethodView

from sqlalchemy import and_

from ..database import db_session
from ..errors import InvalidUsage
from ..forms.nutrient_forms import CreateNutrientForm, \
    get_n_pattern2_choices
from ..models.nutrient_models import Nutrient, NutrientPattern,\
    FactorSet, Factor
from ..models.unit_models import UnitCommon


class NutrientAPI(MethodView):

    def __init__(self, template):
        self.template = template

    def get(self, nutrient_code) -> object:
        if nutrient_code is None:
            dt_pattern = request.values.get('dt_pattern')
            pattern1 = request.values.get('pattern1')
            list_data = []
            if dt_pattern is None:
                raise InvalidUsage('There is no dt_pattern.', status_code=410)
            elif pattern1 is None:
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.is_active == True
                ).all()
            else:
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.pattern1 == pattern1,
                    Nutrient.is_active == True
                ).all()
            nutrients_len = len(list_data)
            return render_template(self.template, nutrients=nutrients,
                                   nutrients_cnt=nutrients_len)
        else:
            dt_pattern, pattern1, pattern2, serial = nutrient_code\
                .split('-')
            form = CreateNutrientForm(request.form)
            if dt_pattern is None:
                return render_template(self.template, form=form)
            else:
                nutrient = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.pattern1 == pattern1,
                    Nutrient.pattern2 == pattern2,
                    Nutrient.serial == serial
                ).first()
                form.pattern2.choices = get_n_pattern2_choices(pattern1)
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
                return render_template(self.template, form=form,
                                       nutrient=nutrient)


class NutrientFormAPI(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self):
        # TODO: Additionally Return Nutrient Obj.
        form = CreateNutrientForm(request.form)
        return render_template(self.template, form=form)


class NutrientPattern2API(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self) -> object:
        pattern1 = request.values.get('pattern1')
        if pattern1 is None:
            raise InvalidUsage('There is no pattern1.', status_code=410)
        else:
            patterns = NutrientPattern.query.filter(
                NutrientPattern.pattern1 == pattern1,
                NutrientPattern.pattern2 != '00',
                NutrientPattern.is_active == True
            ).all()
            option = {'input_type': 'radio', 'input_name': 'pattern2'}
            return render_template(self.template, patterns=patterns, option=option)


class FactorSetAPI(MethodView):

    def __init__(self, template):
        self.template = template

    def get(self) -> object:
        requests = request.args
        dt_pattern = requests.get('dt_pattern')
        pattern1 = requests.get('pattern1')
        pattern2 = requests.get('pattern2')
        serial = requests.get('serial')

        # Get Selected Nutrient's Factors.
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
        factors_len = len(factors)

        # Get A Selected Nutrient Info.
        nutrient = Nutrient.query.filter(
            Nutrient.dt_pattern == dt_pattern,
            Nutrient.pattern1 == pattern1,
            Nutrient.pattern2 == pattern2,
            Nutrient.serial == serial
        ).first()

        return render_template(self.template, factors=factors,
                               factors_cnt=factors_len, nutrient=nutrient)


class FactorAPI(MethodView):
    def __init__(self, templates):
        self.initial_tpl = templates['initial']
        self.table_tpl = templates['table']
        self.opted_tpl = templates['opted']

    def get(self, factor_code) -> object:

        # Gives a list of factors.
        if factor_code is None:
            factors = []
            request_type = request.values.get('request_type')
            pattern1 = request.values.get('pattern1')
            pattern2 = request.values.get('pattern2')
            pattern3 = request.values.get('pattern3')
            pattern4 = request.values.get('pattern4')

            if request_type == 'initial':
                factors = Factor.query.filter(
                    Factor.pattern2 == '0',
                ).all()
                template = self.initial_tpl
            elif request_type == 'addition':
                factors = Factor.query.filter(
                    Factor.pattern1 == pattern1,
                    Factor.pattern2 == pattern2,
                    Factor.pattern3 == pattern3,
                    Factor.pattern4 == pattern4
                ).all()
                template = self.table_tpl

            factors_len = len(factors)
            return render_template(template, factors=factors,
                                   factors_cnt=factors_len)

        # Shows a single factor.
        else:
            values = request.values
            pattern1 = values.get('pattern1')
            pattern2 = values.get('pattern2')
            pattern3 = values.get('pattern3')
            pattern4 = values.get('pattern4')
            factor = Factor.query.filter(
                Factor.pattern1 == pattern1,
                Factor.pattern2 == pattern2,
                Factor.pattern3 == pattern3,
                Factor.pattern4 == pattern4
            ).first()
            units = UnitCommon.query.filter(
                UnitCommon.pattern1 == 'ma'
            ).all()
            return render_template(self.opted_tpl, factor=factor, units=units)

    # Creates a new set of factor what depends on nutrient.
    def post(self):
        factor_code = request.values.get("factor_code")
        nutrient_code = request.values.get("nutrient_code")
        f_pattern1, f_pattern2, f_pattern3, f_pattern4 = \
            factor_code.split('-')
        n_dt_pattern, n_pattern1, n_pattern2, n_serial = \
            nutrient_code.split('-')


