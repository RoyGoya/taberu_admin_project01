from flask import request, render_template
from flask.views import MethodView

from ..errors import InvalidUsage
from ..forms.nutrient_forms import CreateNutrientForm, get_n_pattern2_choices
from ..models.nutrient_models import Nutrient, NutrientPattern


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


class NutrientFormAPI(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self, nutrient_code):
        if nutrient_code is None:
            form = CreateNutrientForm(request.form)
            return render_template(self.template, form=form)
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

