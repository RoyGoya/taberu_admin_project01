# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/


from flask import render_template, request
from flask.views import View

from sqlalchemy import and_

from ..models.tag_models import Tag, TagSet
from ..models.nutrition_models import Nutrition, NutritionSet
from ..helpers.secu_redir import redirect_back


class NutritionListView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        nutritions = Nutrition.query.filter_by(dt_pattern='s',
                                               is_active=True).all()
        return render_template(self.template_name, nutritions=nutritions)


class NutritionDetailView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        if request.method == 'POST':
            form = request.form
            selected_nutrition_name = form.get('selected_nutrition_name')
            subq = NutritionSet.query.filter_by(
                super_nutrition_dt_pattern=form.get('dt_pattern'),
                super_nutrition_nt_pattern1=form.get('nt_pattern1'),
                super_nutrition_nt_pattern2=form.get('nt_pattern2'),
                super_nutrition_serial=form.get('serial')
            ).subquery()
            nutritions = Nutrition.query.join(subq, and_(
                subq.c.sub_nutrition_dt_pattern == Nutrition.dt_pattern,
                subq.c.sub_nutrition_nt_pattern1 == Nutrition.nt_pattern1,
                subq.c.sub_nutrition_nt_pattern2 == Nutrition.nt_pattern2,
                subq.c.sub_nutrition_serial == Nutrition.serial
            )).all()

            return render_template(
                self.template_name,
                selected_nutrition_name=selected_nutrition_name,
                nutritions=nutritions)
        else:
            return redirect_back('index_page')
