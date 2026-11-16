"""Only the entry page and an authenticated welcome page are in this phase."""
from datetime import date
from flask import Blueprint, g, redirect, render_template, url_for
from .auth import login_required
from app.repository import profiles, scholarships

bp = Blueprint('main', __name__)


@bp.get('/')
def home():
    items = scholarships.list_all()
    return render_template('home.html', items=items[:3], scholarship_count=len(items), today=date.today())


@bp.get('/welcome')
@login_required
def welcome():
    return redirect(url_for('main.dashboard'))


@bp.get('/dashboard')
@login_required
def dashboard():
    if g.user['role'] == 'admin':
        return redirect(url_for('admin.index'))
    profile = profiles.find(g.user['id'])
    items = scholarships.list_all()
    profile_fields = ('degree', 'field', 'cgpa', 'age', 'nationality', 'preferred_country', 'preferred_funding')
    completed_fields = sum(1 for field in profile_fields if profile and profile.get(field) not in (None, ''))
    profile_progress = round(completed_fields / len(profile_fields) * 100)
    return render_template('dashboard.html', profile=profile, items=items[:3],
                           scholarship_count=len(items), profile_progress=profile_progress, today=date.today())
