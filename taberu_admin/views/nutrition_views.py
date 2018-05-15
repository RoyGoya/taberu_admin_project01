# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/


from flask import render_template, request
from flask.views import View

from sqlalchemy import and_

from ..models.tag_models import Tag, TagSet
from ..models.nutrition_models import Nutrition, NutritionSet, \
    NutritionFactor, NutritionFactorSet
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

            # Get Selected Nutrition's Components from db.
            nset_subq = NutritionSet.query.filter_by(
                super_nutrition_dt_pattern=form.get('dt_pattern'),
                super_nutrition_nt_pattern1=form.get('nt_pattern1'),
                super_nutrition_nt_pattern2=form.get('nt_pattern2'),
                super_nutrition_serial=form.get('serial')
            ).subquery()
            nutritions = Nutrition.query.join(nset_subq, and_(
                nset_subq.c.sub_nutrition_dt_pattern == Nutrition.dt_pattern,
                nset_subq.c.sub_nutrition_nt_pattern1 == Nutrition.nt_pattern1,
                nset_subq.c.sub_nutrition_nt_pattern2 == Nutrition.nt_pattern2,
                nset_subq.c.sub_nutrition_serial == Nutrition.serial
            )).all()

            # Get Selected Nutrition's Factors from db.
            fset_suq = NutritionFactorSet.query.filter_by(
                nutrition_dt_pattern=form.get('dt_pattern'),
                nutrition_nt_pattern1=form.get('nt_pattern1'),
                nutrition_nt_pattern2=form.get('nt_pattern2'),
                nutrition_serial=form.get('serial')
            ).subquery()
            factors = NutritionFactor.query.join(fset_suq, and_(
                fset_suq.c.nf_pattern1 == NutritionFactor.pattern1,
                fset_suq.c.nf_pattern2 == NutritionFactor.pattern2,
                fset_suq.c.nf_pattern3 == NutritionFactor.pattern3,
                fset_suq.c.nf_pattern4 == NutritionFactor.pattern4
            )).all()

            return render_template(
                self.template_name,
                selected_nutrition_name=selected_nutrition_name,
                nutritions=nutritions, factors=factors)
        else:
            return redirect_back('index_page')
