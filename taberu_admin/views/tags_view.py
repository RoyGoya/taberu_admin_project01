# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/


from flask import render_template, request
from flask.views import View

from ..models.tags_model import Tag
from ..helpers.secu_redir import get_redirect_target, redirect_back


class TagListView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        tags = Tag.query.filter_by(dt_pattern='s', pattern='i'
                                   , is_set=True).all()
        return render_template(self.template_name, tags=tags)


class TagDetailView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = request.form
        if request.method == 'POST':
            selected_tag_name = form.get('selected_tag_name')
            tags = Tag.query.filter_by(dt_pattern=form.get('dt_pattern'),
                                       pattern=form.get('pattern'),
                                       serial=form.get('serial'),
                                       is_active=True)
            return render_template(self.template_name
                                   , selected_tag_name=selected_tag_name
                                   , tags=tags)
        else:
            return redirect_back('index_page')
