"""Only the entry page and an authenticated welcome page are in this phase."""
from datetime import date
from flask import Blueprint, g, redirect, render_template, url_for
from .auth import login_required
from app.repository import profiles, scholarships

bp = Blueprint('main', __name__)


@bp.get('/')
def home():
    return render_template('home.html', items=scholarships.list_all()[:3], today=date.today())


@bp.get('/welcome')
@login_required
def welcome():
    return redirect(url_for('main.dashboard'))


@bp.get('/dashboard')
@login_required
def dashboard():
    profile = profiles.find(g.user['id'])
    items = scholarships.list_all()
    return render_template('dashboard.html', profile=profile, items=items[:3],
                           scholarship_count=len(items), today=date.today())
