"""Pluggable Views

http://flask.pocoo.org/docs/0.12/views/"""

from flask import render_template, request, flash, redirect, url_for
from flask.views import View

from sqlalchemy import and_

from ..database import db_session
from ..forms.nutrient_forms import CreateNutrientForm
from ..models.nutrient_models import Nutrient, NutrientSet, \
    Factor, FactorSet
from ..helpers.secu_redir import redirect_back


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


class DetailNutritionView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        if request.method == 'POST':
            form = request.form
            selected_nutrition_name = form.get('selected_nutrition_name')

            # Get Selected Nutrition's Components from db.
            nset_subq = NutrientSet.query.filter_by(
                super_dt_pattern=form.get('dt_pattern'),
                super_pattern1=form.get('pattern1'),
                super_pattern2=form.get('pattern2'),
                super_serial=form.get('serial')
            ).subquery()
            nutritions = Nutrient.query.join(nset_subq, and_(
                nset_subq.c.sub_nutrient_dt_pattern == Nutrient.dt_pattern,
                nset_subq.c.sub_nutrient_pattern1 == Nutrient.pattern1,
                nset_subq.c.sub_nutrient_pattern2 == Nutrient.pattern2,
                nset_subq.c.sub_nutrient_serial == Nutrient.serial
            )).all()

            # Get Selected Nutrition's Factors from db.
            fset_suq = FactorSet.query.filter_by(
                nutrient_dt_pattern=form.get('dt_pattern'),
                nutrient_pattern1=form.get('pattern1'),
                nutrient_pattern2=form.get('pattern2'),
                nutrient_serial=form.get('serial')
            ).subquery()
            factors = Factor.query.join(fset_suq, and_(
                fset_suq.c.factor_pattern1 == Factor.pattern1,
                fset_suq.c.factor_pattern2 == Factor.pattern2,
                fset_suq.c.factor_pattern3 == Factor.pattern3,
                fset_suq.c.factor_pattern4 == Factor.pattern4
            )).all()

            return render_template(
                self.template_name,
                selected_nutrition_name=selected_nutrition_name,
                nutritions=nutritions, factors=factors)
        else:
            return redirect_back('index_page')


class CreateNutritionView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = CreateNutrientForm(request.form)
        nutrients = Nutrient.query.filter(Nutrient.dt_pattern == 's',
                                          Nutrient.is_active == True).all()
        if request.method == 'POST' and form.validate():
            nutrition_serial = int(Nutrient.query.filter_by(
                dt_pattern=form.dt_pattern, nt_pattern1=form.pattern1,
                nt_pattern2=form.pattern2).count()) + 1
            nutrient = Nutrient(dt_pattern=form.dt_pattern,
                                 pattern1=form.pattern1,
                                 pattern2=form.pattern2,
                                 serial=nutrition_serial,
                                 is_active=True, has_sub=form.has_sub,
                                 eng_name=form.eng_name,
                                 eng_plural=form.eng_plural,
                                 kor_name=form.kor_name,
                                 jpn_name=form.jpn_name,
                                 chn_name=form.chn_name, )
            db_session.add(nutrient)
            db_session.commit()
            flash('Nutrition created successfully.')
            nutrient_form = {"dt_pattern": nutrient.dt_pattern,
                              "pattern1": nutrient.pattern1,
                              "pattern2": nutrient.pattern2,
                              "serial": nutrient.serial,
                              "selected_nutrition_name": nutrient.eng_name}
            return redirect(url_for('detail_nutrition_page', nutrient_form))
        return render_template(self.template_name, form=form,
                               nutrients=nutrients)
