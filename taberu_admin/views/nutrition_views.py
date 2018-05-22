"""Pluggable Views

http://flask.pocoo.org/docs/0.12/views/"""

from flask import render_template, request, flash, redirect, url_for
from flask.views import View

from sqlalchemy import and_

from ..database import db_session
from ..forms.nutrition_forms import CreateNutritionForm
from ..models.nutrition_models import Nutrition, NutritionSet, \
    NutritionFactor, NutritionFactorSet
from ..helpers.secu_redir import redirect_back


class NutritionView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = CreateNutritionForm(request.form)
        nutrition_list = Nutrition.query.filter(Nutrition.dt_pattern=='s',
                                                 Nutrition.is_active==True
                                                 ).all()
        nutrition_list_len = len(nutrition_list)
        return render_template(self.template_name, form=form,
                               nutrition_list=nutrition_list,
                               nutrition_list_cnt=nutrition_list_len)


class DetailNutritionView(View):
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
                super_nutrition_nt_pattern1=form.get('pattern1'),
                super_nutrition_nt_pattern2=form.get('pattern2'),
                super_nutrition_serial=form.get('serial')
            ).subquery()
            nutritions = Nutrition.query.join(nset_subq, and_(
                nset_subq.c.sub_nutrition_dt_pattern == Nutrition.dt_pattern,
                nset_subq.c.sub_nutrition_nt_pattern1 == Nutrition.pattern1,
                nset_subq.c.sub_nutrition_nt_pattern2 == Nutrition.pattern2,
                nset_subq.c.sub_nutrition_serial == Nutrition.serial
            )).all()

            # Get Selected Nutrition's Factors from db.
            fset_suq = NutritionFactorSet.query.filter_by(
                nutrition_dt_pattern=form.get('dt_pattern'),
                nutrition_nt_pattern1=form.get('pattern1'),
                nutrition_nt_pattern2=form.get('pattern2'),
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


class CreateNutritionView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = CreateNutritionForm(request.form)
        nutrition_packs = Nutrition.query.filter(Nutrition.dt_pattern=='s',
                                                 Nutrition.is_active==True
                                                 ).all()
        if request.method == 'POST' and form.validate():
            nutrition_serial = int(Nutrition.query.filter_by(
                dt_pattern=form.dt_pattern, nt_pattern1=form.pattern1,
                nt_pattern2=form.pattern2).count()) + 1
            nutrition = Nutrition(dt_pattern=form.dt_pattern,
                                  pattern1=form.pattern1,
                                  pattern2=form.pattern2,
                                  serial=nutrition_serial,
                                  is_active=True, has_sub=form.has_sub,
                                  eng_name=form.eng_name,
                                  eng_plural=form.eng_plural,
                                  kor_name=form.kor_name,
                                  jpn_name=form.jpn_name,
                                  chn_name=form.chn_name, )
            db_session.add(nutrition)
            db_session.commit()
            flash('Nutrition created successfully.')
            nutrition_form = {"dt_pattern": nutrition.dt_pattern,
                              "pattern1": nutrition.pattern1,
                              "pattern2": nutrition.pattern2,
                              "serial": nutrition.serial,
                              "selected_nutrition_name": nutrition.eng_name}
            return redirect(url_for('detail_nutrition_page', nutrition_form))
        return render_template(self.template_name, form=form,
                               nutrition_packs=nutrition_packs)
