"""Validate and save the current student's academic profile."""
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from app.blueprints.auth import login_required
from app.repository import profiles
from app import validation as v

bp = Blueprint('profile', __name__)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def edit():
    values, errors = profiles.find(g.user['id']) or {}, {}
    if request.method == 'POST':
        values = request.form.to_dict()
        data = {
            'degree': v.choice(request.form, 'degree', v.DEGREES, errors, 'target degree'),
            'field': v.choice(request.form, 'field', v.FIELDS, errors, 'field'),
            'cgpa': v.number(request.form, 'cgpa', errors, 'CGPA', 0, 4),
            'age': v.number(request.form, 'age', errors, 'Age', 16, 100, integer=True),
            'nationality': v.text(request.form, 'nationality', errors, 'Nationality', maximum=80),
            'preferred_country': v.choice(request.form, 'preferred_country', ('any',) + v.COUNTRIES, errors, 'preferred country'),
            'preferred_funding': v.choice(request.form, 'preferred_funding', ('any',) + tuple(v.FUNDING), errors, 'funding preference'),
        }
        if data['nationality'] and not all(c.isalpha() or c in " -'" for c in data['nationality']):
            errors['nationality'] = 'Use letters, spaces, apostrophes or hyphens for nationality.'
        if not errors:
            profiles.save(g.user['id'], data)  # Ignore any user_id supplied by the browser.
            flash('Your academic profile has been saved.', 'success')
            return redirect(url_for('main.dashboard'))
    return render_template('profile.html', values=values, errors=errors), 400 if errors else 200
