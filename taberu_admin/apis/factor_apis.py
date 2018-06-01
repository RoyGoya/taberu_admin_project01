from flask import request, render_template, flash
from flask.views import MethodView

from sqlalchemy import and_
from sqlalchemy.orm import joinedload, subqueryload

from ..database import db_session
from ..errors import InvalidUsage
from ..models.nutrient_models import Nutrient
from ..models.factor_models import Factor, FactorSet
from ..models.unit_models import UnitCommon
from ..forms.factor_forms import UpdateFactorForm


def get_unit_choices():
    choice_tuple_list = []
    units = UnitCommon.query.filter(
        UnitCommon.pattern1 == 'ma'
    ).all()
    for unit in units:
        choice_tuple = ((unit.pattern1+'-'+unit.pattern2), unit.symbol)
        choice_tuple_list += {choice_tuple}
    return choice_tuple_list


class FactorAPI(MethodView):
    def __init__(self, templates):
        self.list_tpl = templates['list']
        self.opted_tpl = templates['opted']

    def get(self, factor_code) -> object:

        # Give all factors.
        if factor_code is None:
            factors = Factor.query.filter(
                Factor.pattern2 == '0',
            ).all()
            factors_len = len(factors)
            return render_template(self.list_tpl, factors=factors,
                                   factors_cnt=factors_len)

        # Shows a single factor.
        else:
            pattern1, pattern2, pattern3, pattern4 = factor_code.split('-')
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


class FactorListAPI(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self, factor_code):
        if factor_code is None:
            raise InvalidUsage('Invalid Request.', status_code=410)

        # Gives A factor-list.
        else:
            pattern1, pattern2, pattern3, pattern4 = factor_code.split('-')
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
            return render_template(self.template, factors=factors)


class FactorSetAPI(MethodView):

    def __init__(self, template):
        self.template = template

    def get(self, nutrient_code) -> object:
        if nutrient_code is None:
            raise InvalidUsage('Invalid Request.', status_code=410)

        # GET: Gives A factor-set.
        else:
            dt_pattern, pattern1, pattern2, serial = nutrient_code.split('-')
            # Get Selected Nutrient's Factors.
            set_of_facotrs = FactorSet.query.filter(
                FactorSet.nutrient_dt_pattern == dt_pattern,
                FactorSet.nutrient_pattern1 == pattern1,
                FactorSet.nutrient_pattern2 == pattern2,
                FactorSet.nutrient_serial == serial
            ).all()
            set_of_facotrs_len = len(set_of_facotrs)

            # Get A Selected Nutrient Info.
            if set_of_facotrs_len <= 0:
                nutrient = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.pattern1 == pattern1,
                    Nutrient.pattern2 == pattern2,
                    Nutrient.serial == serial
                ).first()
            else:
                nutrient = set_of_facotrs[0].nutrient

            return render_template(self.template, set_of_facotrs=set_of_facotrs,
                                   set_of_facotrs_cnt=set_of_facotrs_len,
                                   nutrient=nutrient)

    # CREATE: Add a new set of factor.
    def post(self):
        factor_code = request.values.get("factor_code")
        nutrient_code = request.values.get("nutrient_code")
        unit_code = request.values.get("unit_code")
        quantity = request.values.get("quantity")
        f_pattern1, f_pattern2, f_pattern3, f_pattern4 = \
            factor_code.split('-')
        n_dt_pattern, n_pattern1, n_pattern2, n_serial = \
            nutrient_code.split('-')
        unit_pattern1, unit_pattern2 = unit_code.split('-')
        factor_set = FactorSet.query.filter(
            FactorSet.nutrient_dt_pattern == n_dt_pattern,
            FactorSet.nutrient_pattern1 == n_pattern1,
            FactorSet.nutrient_pattern2 == n_pattern2,
            FactorSet.nutrient_serial == n_serial,
            FactorSet.factor_pattern1 == f_pattern1,
            FactorSet.factor_pattern2 == f_pattern2,
            FactorSet.factor_pattern3 == f_pattern3,
            FactorSet.factor_pattern4 == f_pattern4,).first()
        if factor_set is None:
            factor_set = FactorSet(nutrient_dt_pattern=n_dt_pattern,
                                   nutrient_pattern1=n_pattern1,
                                   nutrient_pattern2=n_pattern2,
                                   nutrient_serial=n_serial,
                                   is_active=True,
                                   factor_pattern1=f_pattern1,
                                   factor_pattern2=f_pattern2,
                                   factor_pattern3=f_pattern3,
                                   factor_pattern4=f_pattern4,
                                   quantity=quantity,
                                   unit_pattern1=unit_pattern1,
                                   unit_pattern2=unit_pattern2)
            db_session.add(factor_set)
            db_session.commit()
            flash('Factor code %r Successfully Inserted.' % factor_code)
            message = 'Success.'
            return message
        else:
            flash('Factor code %r Already taken.' % factor_code)
            message = 'Fail.'
            return message


class SetOfAFactorAPI(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self, factor_set_code):
        if factor_set_code is None:
            raise InvalidUsage('Invalid Request.', status_code=410)
        else:
            n_dt_pattern, n_pattern1, n_pattern2, n_serial, f_pattern1, f_pattern2, \
            f_pattern3, f_pattern4 = factor_set_code.split('-')
            factor_set = FactorSet.query.filter(
                FactorSet.nutrient_dt_pattern == n_dt_pattern,
                FactorSet.nutrient_pattern1 == n_pattern1,
                FactorSet.nutrient_pattern2 == n_pattern2,
                FactorSet.nutrient_serial == n_serial,
                FactorSet.factor_pattern1 == f_pattern1,
                FactorSet.factor_pattern2 == f_pattern2,
                FactorSet.factor_pattern3 == f_pattern3,
                FactorSet.factor_pattern4 == f_pattern4, ).first()

            form = UpdateFactorForm(request.form)
            form.unit.choices = get_unit_choices()
            unit = factor_set.unit
            form.unit.data = (unit.pattern1 + '-' + unit.pattern2)
            return render_template(self.template, form=form, factor_set=factor_set)
