"""Pluggable Views

http://flask.pocoo.org/docs/0.12/views/"""

from flask import render_template, request
from flask.views import View

from ..forms.nutrient_forms import CreateNutrientForm
from ..models.nutrient_models import Nutrient


class NutritionView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = CreateNutrientForm(request.form)
        nutrients = Nutrient.query.filter(Nutrient.dt_pattern == 's',
                                          Nutrient.is_active == True).all()
        nutrient_len = len(nutrients)
        return render_template(self.template_name, form=form,
                               nutrients=nutrients,
                               nutrients_cnt=nutrient_len)
