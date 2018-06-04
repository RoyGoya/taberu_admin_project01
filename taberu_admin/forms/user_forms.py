# WTForms
# http://flask.pocoo.org/docs/1.0/patterns/wtforms/


from wtforms import Form, BooleanField, StringField, PasswordField, \
    validators, SubmitField

from taberu_admin.models.user_models import User


class RegistrationForm(Form):
    first_name = StringField('First name', [
        validators.DataRequired(message="Please enter your first name."),
        validators.Length(min=2, max=30)
    ])
    last_name = StringField('Last name', [
        validators.DataRequired(message="Please enter your last name."),
        validators.Length(min=2, max=30)
    ])
    email = StringField('Email Address', [validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class LoginForm(Form):
    email = StringField('Email Address', [validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
