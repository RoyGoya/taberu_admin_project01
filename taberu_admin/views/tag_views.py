# Pluggable Views
# http://flask.pocoo.org/docs/0.12/views/


from flask import render_template, request
from flask.views import View

from sqlalchemy import and_

from ..models.tag_models import Tag, TagSet
from ..helpers.secu_redir import redirect_back


class TagListView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        tags = Tag.query.filter_by(dt_pattern='s', pattern='i',
                                   is_set=True).all()
        return render_template(self.template_name, tags=tags)


class TagDetailView(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        form = request.form
        if request.method == 'POST':
            selected_tag_name = form.get('selected_tag_name')
            subq = TagSet.query.filter_by(
                super_tag_dt_pattern=form.get('dt_pattern'),
                super_tag_pattern=form.get('pattern'),
                super_tag_serial=form.get('serial'),
                is_active=True).subquery()
            tags = Tag.query.join(subq, and_(
                subq.c.sub_tag_dt_pattern == Tag.dt_pattern,
                subq.c.sub_tag_pattern == Tag.pattern,
                subq.c.sub_tag_serial == Tag.serial
            )).all()

            return render_template(self.template_name,
                                   selected_tag_name=selected_tag_name,
                                   tags=tags)
        else:
            return redirect_back('index_page')
