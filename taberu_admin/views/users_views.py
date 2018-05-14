# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/


from flask import render_template, request, flash, redirect, url_for
from flask.views import View

from flask_login import login_user, logout_user

from ..database import db_session
from ..forms.user_forms import RegistrationForm, LoginForm
from ..models.user_models import User
from ..helpers.secu_redir import get_redirect_target, redirect_back
from ..helpers.auth_admin import is_admin


class RegisterView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            user = User(email=form.email.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        password=form.password.data)
            db_session.add(user)
            db_session.commit()
            flash('Thanks for registering.')
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('profile_page'))
        return render_template(self.template_name, form=form)


class LoginView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            user = User(form.email.data, form.password.data)
            if is_admin(user) is True:
                login_user(user, remember=False)
                # Remember me
                # login_user(user, remember=True)
                flash('Logged in successfully.')
                next_page = get_redirect_target()
                return redirect_back(next_page or 'index_page')
            else:
                return render_template(self.template_name, form=form)
        else:
            return render_template(self.template_name, form=form)


class LogoutView(View):
    methods = ['GET', 'POST']

    def __init__(self, next_url):
        self.next_url = next_url

    def dispatch_request(self):
        logout_user()
        return redirect(url_for(self.next_url))


class ProfileView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)


class ManageUsersView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)
