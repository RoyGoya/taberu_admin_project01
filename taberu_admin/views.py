from flask import render_template, request
from flask.views import View

from taberu_admin.forms.nutrient_forms import CreateNutrientForm
from taberu_admin.models.nutrient_models import Nutrient
from taberu_admin.apis.nutrient_apis import get_dt_pattern_choices, get_n_pattern1_choices


class IndexView(View):
    def __init__(self, template):
        self.template = template

    def dispatch_request(self):
        return render_template(self.template)


class NutrientView(View):
    def __init__(self, template):
        self.template = template

    def dispatch_request(self):
        form = CreateNutrientForm(request.form)
        nutrients = Nutrient.query.filter(Nutrient.dt_pattern == 's').all()
        form.dt_pattern.choices = get_dt_pattern_choices()
        form.pattern1.choices = get_n_pattern1_choices()
        form.pattern2.choices = []
        form.dt_pattern.data = 's'
        nutrient_len = len(nutrients)
        return render_template(self.template, form=form,
                               nutrients=nutrients,
                               nutrients_cnt=nutrient_len)
