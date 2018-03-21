# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/


from flask import render_template
from flask.views import View


class IndexView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)
