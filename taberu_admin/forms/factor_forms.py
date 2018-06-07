from wtforms import Form, StringField, validators, SelectField


class SelectUnitForm(Form):
    unit = SelectField()
    quantity = StringField(validators=[validators.NumberRange(min=0, max=None)])
