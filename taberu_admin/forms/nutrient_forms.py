# WTForms
# http://flask.pocoo.org/docs/1.0/patterns/wtforms/


from wtforms import Form, BooleanField, StringField, PasswordField, \
    validators, SubmitField, RadioField


class CreateNutrientForm(Form):

    """Field Class's Parameters
    (self, label=None, validators=None, filters=tuple(),
    description='', id=None, default=None, widget=None,
    render_kw=None, _form=None, _name=None, _prefix='',
    _translations=None, _meta=None):
    """
    dt_pattern = RadioField(label="DataType", choices=[])
    pattern1 = RadioField(label="Pattern1", choices=[])
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
