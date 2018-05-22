# WTForms
# http://flask.pocoo.org/docs/1.0/patterns/wtforms/


from wtforms import Form, BooleanField, StringField, PasswordField, \
    validators, SubmitField, RadioField

from ..models.nutrition_models import NutritionPattern, DataPattern


def get_dt_pattern_choices():
    choice_tuple_list = []
    data_patterns = DataPattern.query.filter_by(is_active=True).all()
    for data_pattern in data_patterns:
        choice_tuple = (data_pattern.pattern, data_pattern.name)
        choice_tuple_list += {choice_tuple}
    return choice_tuple_list


def get_nutrition_pattern1_choices():
    choice_tuple_list = []
    nutrition_patterns = NutritionPattern.query.filter_by(pattern2='00',
                                                          is_active=True).all()
    for nutrition_pattern in nutrition_patterns:
        choice_tuple = (nutrition_pattern.pattern1, nutrition_pattern.eng_name)
        choice_tuple_list += {choice_tuple}
    return choice_tuple_list


def get_nutrition_pattern2_choices(pattern1):
    choice_tuple_list = []
    nutrition_patterns = NutritionPattern.query.filter(
        NutritionPattern.pattern1 == pattern1,
        NutritionPattern.pattern2 != '00',
        NutritionPattern.is_active == True
    ).all()

    for nutrition_pattern in nutrition_patterns:
        choice_tuple = (nutrition_pattern.pattern2, nutrition_pattern.eng_name)
        choice_tuple_list += {choice_tuple}
    return choice_tuple_list


class CreateNutritionForm(Form):

    """Field Class's Parameters
    (self, label=None, validators=None, filters=tuple(),
    description='', id=None, default=None, widget=None,
    render_kw=None, _form=None, _name=None, _prefix='',
    _translations=None, _meta=None):
    """
    dt_pattern_choices = get_dt_pattern_choices()
    dt_pattern = RadioField(label="DataType", choices=dt_pattern_choices,
                            default=dt_pattern_choices[0][0])
    pattern1 = RadioField(label="Pattern1",
                             choices=get_nutrition_pattern1_choices())
    pattern2 = RadioField(label="Pattern2", choices=[])
    has_sub = RadioField(label="Has Sub?", choices=[
        (True, 'True'), (False, 'False')
    ])
    is_active = RadioField(label="Is Active?", choices=[
        (True, 'True'), (False, 'False')
    ])
    eng_name = StringField(label="English Name", validators=[
        validators.DataRequired("Please Enter A English Name."),
        validators.Length(min=2, max=100)
    ])
    eng_plural = StringField(label="English plural", validators=[
        validators.Length(min=2, max=100)
    ])
    kor_name = StringField(label="Korean Name", validators=[
        validators.Length(min=2, max=100)
    ])
    jpn_name = StringField(label="Japanese Name", validators=[
        validators.Length(min=2, max=100)
    ])
    chn_name = StringField(label="Chinese Name", validators=[
        validators.Length(min=2, max=100)
    ])
