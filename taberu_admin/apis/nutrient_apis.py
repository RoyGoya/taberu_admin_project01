from flask import request, render_template, redirect, url_for
from flask.views import MethodView

from ..database import db_session
from ..errors import InvalidUsage
from ..forms.nutrient_forms import CreateNutrientForm
from ..models.nutrient_models import Nutrient, NutrientPattern, DataPattern


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


class NutrientAPI(MethodView):

    def __init__(self, template):
        self.template = template

    def get(self, nutrient_code) -> object:
        if nutrient_code is None:
            raise InvalidUsage('There is no dt_pattern.', status_code=410)
        else:
            # Return a list of nutrients.
            code_len = len(nutrient_code.split('-'))
            if code_len == 1:
                dt_pattern = nutrient_code
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.is_active == True
                ).all()
            elif code_len == 2:
                [dt_pattern, pattern1] = nutrient_code.split('-')
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.pattern1 == pattern1,
                    Nutrient.is_active == True
                ).all()
            elif code_len == 3:
                [dt_pattern, pattern1, pattern2] = nutrient_code.split('-')
                nutrients = Nutrient.query.filter(
                    Nutrient.dt_pattern == dt_pattern,
                    Nutrient.pattern1 == pattern1,
                    Nutrient.pattern2 == pattern2,
                    Nutrient.is_active == True
                ).all()

            nutrients_len = len(nutrients)
            return render_template(self.template, nutrients=nutrients,
                                   nutrients_cnt=nutrients_len)

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
        pass

    def put(self, nutrient_code):
        # TODO: Refactor this
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
        )
        nutrient.has_sub = has_sub
        nutrient.is_active = is_active
        nutrient.eng_name = form.eng_name.data
        nutrient.eng_plural = form.eng_plural.data
        nutrient.kor_name = form.kor_name.data
        nutrient.jpn_name = form.jpn_name.data
        nutrient.chn_name = form.chn_name.data
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


class NutrientPattern2API(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self, pattern1_code):
        if pattern1_code is None:
            pass
        else:
            pattern1 = pattern1_code
            if pattern1 is None:
                raise InvalidUsage('There is no pattern1.', status_code=410)
            else:
                patterns = NutrientPattern.query.filter(
                    NutrientPattern.pattern1 == pattern1,
                    NutrientPattern.pattern2 != '00',
                    NutrientPattern.is_active == True
                ).all()
                option = {'input_type': 'radio', 'input_name': 'pattern2'}
                return render_template(self.template, patterns=patterns,
                                       option=option)
