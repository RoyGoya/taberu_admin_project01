from wtforms import Form, StringField, validators, SelectField


class UpdateFactorForm(Form):
    unit = SelectField()
    quantity = StringField(validators=[validators.NumberRange(min=0, max=None)])
