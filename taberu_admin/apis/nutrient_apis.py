from flask import request, render_template, redirect, url_for
from flask.views import MethodView

from sqlalchemy import or_

from ..database import db_session
from ..errors import InvalidUsage
from ..forms.nutrient_forms import CreateNutrientForm, NutrientOptionForm, \
    NutrientPattern2Form
from ..forms.factor_forms import SelectUnitForm
from ..models.nutrient_models import Nutrient, NutrientPattern, DataPattern, \
    NutrientSet
from ..models.unit_models import UnitCommon


def get_dt_pattern_choices():
    choice_tuple_list = []
    data_patterns = DataPattern.query.filter_by(is_active=True).all()
    for data_pattern in data_patterns:
        choice_tuple = (data_pattern.pattern, data_pattern.name)
        choice_tuple_list += {choice_tuple}
    return choice_tuple_list


def get_n_pattern1_choices():
    choice_tuple_list = []
    nutrient_patterns = NutrientPattern.query.filter(
        NutrientPattern.pattern2 == '00',
        NutrientPattern.is_active == True).all()
    for nutrient_pattern in nutrient_patterns:
        choice_tuple = (nutrient_pattern.pattern1, nutrient_pattern.eng_name)
        choice_tuple_list += {choice_tuple}
    return choice_tuple_list


def get_n_pattern2_choices(pattern1):
    choice_tuple_list = []
    nutrient_patterns = NutrientPattern.query.filter(
        NutrientPattern.pattern1 == pattern1,
        NutrientPattern.pattern2 != '00',
        NutrientPattern.is_active == True
    ).all()

    for nutrient_pattern in nutrient_patterns:
        choice_tuple = (nutrient_pattern.pattern2, nutrient_pattern.eng_name)
        choice_tuple_list += {choice_tuple}
    return choice_tuple_list


def get_unit_choices():
    choice_tuple_list = []
    units = UnitCommon.query.filter(
        or_(UnitCommon.pattern1 == 'ma', UnitCommon.pattern1 == 'vl')
    ).all()
    for unit in units:
        choice_tuple = ((unit.pattern1+'-'+unit.pattern2), unit.symbol)
        choice_tuple_list += {choice_tuple}
    return choice_tuple_list


class NutrientAPI(MethodView):

    def __init__(self, templates):
        self.list_tpl = templates['list']
        self.get_tpl = templates['get']
        self.opted_tpl = templates['opted']
        self.table_tpl = templates['table']

    def get(self, nutrient_code) -> object:
        # Return a list of nutrients.
        if nutrient_code is None:
            dt_pattern = request.values.get('dt_pattern')
            pattern1 = request.values.get('pattern1')
            pattern2 = request.values.get('pattern2')
            serial = request.values.get('serial')
            if dt_pattern is None:
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == 's',
                ).all()
            elif pattern1 is None:
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                ).all()
            elif pattern2 is None:
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.pattern1 == pattern1,
                ).all()
            elif serial is None:
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.pattern1 == pattern1,
                    Nutrient.pattern2 == pattern2,
                ).all()
            nutrients_len = len(nutrients)
            return render_template(self.table_tpl, nutrients=nutrients,
                                   nutrients_cnt=nutrients_len)

        else:
            # Return a single nutrient.
            [dt_pattern, pattern1, pattern2, serial] = nutrient_code.split('-')
            nutrient = Nutrient.query.filter(
                Nutrient.dt_pattern == dt_pattern,
                Nutrient.pattern1 == pattern1,
                Nutrient.pattern2 == pattern2,
                Nutrient.serial == serial
            ).first()
            form = SelectUnitForm()
            form.unit.choices = get_unit_choices()
            return render_template(self.opted_tpl, nutrient=nutrient, form=form)

    def post(self):
        # Create a new nutrient.
        form = CreateNutrientForm(request.form)
        nutrient_cnt = Nutrient.query.filter(
            Nutrient.dt_pattern == form.dt_pattern.data,
            Nutrient.pattern1 == form.pattern1.data,
            Nutrient.pattern2 == form.pattern2.data
        ).count()

        if form.has_sub.data == 'True':
            has_sub = True
        else:
            has_sub = False
        if form.is_active.data == 'True':
            is_active = True
        else:
            is_active = False

        nutrient = Nutrient(
            dt_pattern=form.dt_pattern.data,
            pattern1=form.pattern1.data,
            pattern2=form.pattern2.data,
            serial=(nutrient_cnt+1),
            has_sub=has_sub,
            is_active=is_active,
            eng_name=form.eng_name.data,
            eng_plural=form.eng_plural.data,
            kor_name=form.kor_name.data,
            jpn_name=form.jpn_name.data,
            chn_name=form.chn_name.data)
        db_session.add(nutrient)
        db_session.commit()
        return redirect(url_for('nutrient_page'))

    def delete(self, nutrient_code):
        # Delete a single nutrient.
        [dt_pattern, pattern1, pattern2, serial] = nutrient_code.split('-')
        nutrient = Nutrient.query.filter(
            Nutrient.dt_pattern == dt_pattern,
            Nutrient.pattern1 == pattern1,
            Nutrient.pattern2 == pattern2,
            Nutrient.serial == serial
        ).first()
        db_session.delete(nutrient)
        db_session.commit()
        message = 'Successfully Deleted.'
        return message

    def put(self, nutrient_code):
        # Update a single nutrient.
        [dt_pattern, pattern1, pattern2, serial] = nutrient_code.split('-')
        form = CreateNutrientForm(request.form)
        if form.has_sub.data == 'True':
            has_sub = True
        else:
            has_sub = False
        if form.is_active.data == 'True':
            is_active = True
        else:
            is_active = False

        nutrient = Nutrient.query.filter(
            Nutrient.dt_pattern == dt_pattern,
            Nutrient.pattern1 == pattern1,
            Nutrient.pattern2 == pattern2,
            Nutrient.serial == serial
        ).first()
        nutrient.has_sub = has_sub
        nutrient.is_active = is_active
        nutrient.eng_name = form.eng_name.data
        nutrient.eng_plural = form.eng_plural.data
        nutrient.kor_name = form.kor_name.data
        nutrient.jpn_name = form.jpn_name.data
        nutrient.chn_name = form.chn_name.data
        db_session.commit()
        message = 'Successfully Updated.'
        return message


class NutrientFormAPI(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self, nutrient_code):
        if nutrient_code is None:
            form = CreateNutrientForm(request.form)
            form.dt_pattern.choices = get_dt_pattern_choices()
            form.pattern1.choices = get_n_pattern1_choices()
            form.pattern2.choices = []
            form.dt_pattern.data = 's'
            return render_template(self.template, form=form)
        else:
            [dt_pattern, pattern1, pattern2, serial] = nutrient_code.split('-')
            form = CreateNutrientForm(request.form)
            form.dt_pattern.choices = get_dt_pattern_choices()
            form.pattern1.choices = get_n_pattern1_choices()
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


class NutrientPatternAPI(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self, pattern1_code):
        if pattern1_code is None:
            pass
        else:
            patterns = NutrientPattern.query.filter(
                NutrientPattern.pattern1 == pattern1_code,
                NutrientPattern.pattern2 != '00',
                NutrientPattern.is_active == True
            ).all()
            option = {'input_type': 'radio', 'input_name': 'pattern2'}
            return render_template(self.template, patterns=patterns,
                                   option=option)


class NutrientSetAPI(MethodView):
    def __init__(self, templates):
        self.sub_tpl = templates['sub']
        self.opted_tpl = templates['opted']

    def get(self, nutrient_set_code):
        if nutrient_set_code is None:
            # Return a set of nutrients.
            nutrient_code = request.values.get('nutrient_code')
            [dt_pattern, pattern1, pattern2, serial] = nutrient_code.split('-')
            nutrient_set = NutrientSet.query.filter(
                NutrientSet.super_dt_pattern == dt_pattern,
                NutrientSet.super_pattern1 == pattern1,
                NutrientSet.super_pattern2 == pattern2,
                NutrientSet.super_serial == serial
            ).all()

            nutrient_set_len = len(nutrient_set)

            if nutrient_set_len <= 0:
                super_nutrient = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.pattern1 == pattern1,
                    Nutrient.pattern2 == pattern2,
                    Nutrient.serial == serial
                ).first()
            else:
                super_nutrient = nutrient_set[0].super_nutrient
            return render_template(self.sub_tpl,
                                   nutrient_set=nutrient_set,
                                   nutrients_cnt=nutrient_set_len,
                                   nutrient=super_nutrient)
        else:
            # Return a set of a single nutrient.
            [super_dt_pattern, super_pattern1, super_pattern2, super_serial,
             sub_dt_pattern, sub_pattern1, sub_pattern2, sub_serial] \
                = nutrient_set_code.split('-')
            nutrient_set = NutrientSet.query.filter(
                NutrientSet.super_dt_pattern == super_dt_pattern,
                NutrientSet.super_pattern1 == super_pattern1,
                NutrientSet.super_pattern2 == super_pattern2,
                NutrientSet.super_serial == super_serial,
                NutrientSet.sub_dt_pattern == sub_dt_pattern,
                NutrientSet.sub_pattern1 == sub_pattern1,
                NutrientSet.sub_pattern2 == sub_pattern2,
                NutrientSet.sub_serial == sub_serial
            ).first()
            nutrient = nutrient_set.nutrient
            form = SelectUnitForm()
            form.unit.choices = get_unit_choices()
            unit = nutrient_set.unit_common
            form.unit.data = (unit.pattern1 + '-' + unit.pattern2)
            form.quantity.data = nutrient_set.quantity
            return render_template(self.opted_tpl, nutrient=nutrient, form=form)

    def post(self):
        # Create a set of new nutrient.
        super_code = request.values.get('super_code')
        sub_code = request.values.get('sub_code')
        unit_code = request.values.get('unit_code')
        quantity = request.values.get('quantity')
        [super_dt_pattern, super_pattern1, super_pattern2, super_serial] = \
            super_code.split('-')
        [sub_dt_pattern, sub_pattern1, sub_pattern2, sub_serial] = \
            sub_code.split('-')
        [unit_pattern1, unit_pattern2] = unit_code.split('-')
        nutrient_set = NutrientSet.query.filter(
            NutrientSet.super_dt_pattern == super_dt_pattern,
            NutrientSet.super_pattern1 == super_pattern1,
            NutrientSet.super_pattern2 == super_pattern2,
            NutrientSet.super_serial == super_serial,
            NutrientSet.sub_dt_pattern == sub_dt_pattern,
            NutrientSet.sub_pattern1 == sub_pattern1,
            NutrientSet.sub_pattern2 == sub_pattern2,
            NutrientSet.sub_serial == sub_serial
        ).first()
        if nutrient_set is None:
            nutrient_set = NutrientSet(super_dt_pattern=super_dt_pattern,
                                       super_pattern1=super_pattern1,
                                       super_pattern2=super_pattern2,
                                       super_serial=super_serial,
                                       sub_dt_pattern=sub_dt_pattern,
                                       sub_pattern1=sub_pattern1,
                                       sub_pattern2=sub_pattern2,
                                       sub_serial=sub_serial,
                                       is_active=True,
                                       unit_pattern1=unit_pattern1,
                                       unit_pattern2=unit_pattern2,
                                       quantity=quantity)
            db_session.add(nutrient_set)
            db_session.commit()
            message = '%r Successfully Added.' % sub_code
            return message
        else:
            message = '%r is Already taken.' % sub_code
            return message

    def delete(self, nutrient_set_code):
        # Delete a set of a single nutrient.
        pass

    def put(self, nutrient_set_code):
        # Update a set of a single nutrient.
        pass


class NutrientOptionFormAPI(MethodView):
    def __init__(self, templates):
        self.option_tpl = templates['option']
        self.pattern2_tpl = templates['pattern2']

    def get(self, pattern1_code):
        if pattern1_code is None:
            form = NutrientOptionForm()
            form.dt_pattern.choices = get_dt_pattern_choices()
            form.dt_pattern.data = 's'
            form.pattern1.choices = get_n_pattern1_choices()
            form.pattern1.choices.insert(0, ('empty', '---'))
            form.pattern2.choices = [('empty', '---')]
            return render_template(self.option_tpl, form=form)
        else:
            form = NutrientPattern2Form()
            form.pattern2.choices = get_n_pattern2_choices(pattern1_code)
            form.pattern2.choices.insert(0, ('empty', '---'))
            return render_template(self.pattern2_tpl, form=form)
