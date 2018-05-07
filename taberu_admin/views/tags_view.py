# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/


from flask import render_template
from flask.views import View

from ..models.tags_model import Tag


class TagListView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        tags = Tag.query.filter_by(dt_pattern='s', pattern='i'
                                   , is_set=True).all()
        return render_template(self.template_name, tags=tags)
