"""Pluggable Views

http://flask.pocoo.org/docs/0.12/views/"""

from flask import render_template, request
from flask.views import View

from ..forms.nutrient_forms import CreateNutrientForm
from ..models.nutrient_models import Nutrient
from ..apis.nutrient_apis import get_dt_pattern_choices, get_n_pattern1_choices


class NutritionView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = CreateNutrientForm(request.form)
        nutrients = Nutrient.query.filter(Nutrient.dt_pattern == 's',
                                          Nutrient.is_active == True).all()
        form.dt_pattern.choices = get_dt_pattern_choices()
        form.pattern1.choices = get_n_pattern1_choices()
        form.dt_pattern.data = 's'
        nutrient_len = len(nutrients)
        return render_template(self.template_name, form=form,
                               nutrients=nutrients,
                               nutrients_cnt=nutrient_len)
