"""Catalogue filters do not claim to determine personal eligibility."""
from datetime import date
from flask import Blueprint, abort, g, render_template, request
from app.repository import scholarships
from app import validation as v

bp = Blueprint('scholarships', __name__, url_prefix='/scholarships')


@bp.get('')
def catalogue():
    filters = {'q': request.args.get('q', '').strip()[:120]}
    for key, options in [('country', v.COUNTRIES), ('degree', v.DEGREES), ('funding', v.FUNDING)]:
        value = request.args.get(key, '')
        filters[key] = value if value in options else ''
    return render_template('catalogue.html', items=scholarships.list_all(filters),
                           filters=filters, today=date.today())


@bp.get('/<int:scholarship_id>')
def detail(scholarship_id):
    item = scholarships.find(scholarship_id)
    if not item or (not item['is_active'] and (not g.user or g.user['role'] != 'admin')):
        abort(404)
    return render_template('detail.html', item=item, today=date.today())
