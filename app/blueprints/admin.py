"""Server-side role checks protect every scholarship management action."""
from functools import wraps
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from app.blueprints.auth import login_required
from app.repository import scholarships
from app import validation as v

bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(view):
    @wraps(view)
    @login_required
    def protected(*args, **kwargs):
        if g.user['role'] != 'admin':
            abort(403)
        return view(*args, **kwargs)
    return protected


@bp.get('')
@admin_required
def index():
    return render_template('admin.html', items=scholarships.list_all(include_archived=True))


def edit_form(scholarship_id=None):
    item = scholarships.find(scholarship_id) if scholarship_id is not None else None
    if scholarship_id is not None and not item:
        abort(404)
    values, errors = item or {'is_active': 1, 'is_sample': 0}, {}
    if request.method == 'POST':
        values = request.form.to_dict()
        data = {
            'title': v.text(request.form, 'title', errors, 'Title', maximum=140),
            'provider': v.text(request.form, 'provider', errors, 'Provider', maximum=120),
            'country': v.choice(request.form, 'country', v.COUNTRIES, errors, 'country'),
            'degree': v.choice(request.form, 'degree', v.DEGREES, errors, 'degree'),
            'field': v.choice(request.form, 'field', ('All fields',) + v.FIELDS, errors, 'field'),
            'funding': v.choice(request.form, 'funding', v.FUNDING, errors, 'funding type'),
            'min_cgpa': v.number(request.form, 'min_cgpa', errors, 'Minimum CGPA', 0, 4),
            'deadline': v.deadline(request.form, errors),
            'description': v.text(request.form, 'description', errors, 'Description', 20, 3000),
            'official_url': request.form.get('official_url', '').strip(),
            'is_active': int(request.form.get('is_active') == 'on'),
            'is_sample': int(request.form.get('is_sample') == 'on'),
        }
        if data['official_url'] and not v.web_url(data['official_url']):
            errors['official_url'] = 'Enter a valid HTTP or HTTPS website address without embedded credentials.'
        elif not data['is_sample'] and not data['official_url']:
            errors['official_url'] = 'An official source link is required for a non-sample record.'
        if not errors:
            saved_id = scholarships.save(data, scholarship_id)
            flash('Scholarship saved.', 'success')
            return redirect(url_for('scholarships.detail', scholarship_id=saved_id))
    return render_template('scholarship_form.html', values=values, errors=errors,
                           editing=scholarship_id is not None), 400 if errors else 200


@bp.route('/scholarships/new', methods=['GET', 'POST'])
@admin_required
def create():
    return edit_form()


@bp.route('/scholarships/<int:scholarship_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(scholarship_id):
    return edit_form(scholarship_id)


@bp.post('/scholarships/<int:scholarship_id>/toggle')
@admin_required
def toggle(scholarship_id):
    if not scholarships.find(scholarship_id):
        abort(404)
    scholarships.toggle_active(scholarship_id)
    flash('Scholarship visibility updated.', 'success')
    return redirect(url_for('admin.index'))
