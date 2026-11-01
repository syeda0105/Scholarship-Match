"""Registration inserts an account. Login verifies an existing account."""
from functools import wraps
import pymysql
from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import generate_password_hash, check_password_hash

from app.repository import users
from app.security import valid_email, safe_next, password_error

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_user():
    g.user = None
    if request.endpoint == 'static':
        return  # Static CSS/JS must still load if MySQL is temporarily unavailable.
    user_id = session.get('user_id')
    if user_id is not None:
        g.user = users.find_by_id(user_id)
        if not g.user or not g.user['is_active']:
            session.clear()
            g.user = None


def login_required(view):
    @wraps(view)
    def protected(*args, **kwargs):
        if g.user is None:
            flash('Please log in to continue.', 'info')
            return redirect(url_for('auth.login', next=request.path))
        return view(*args, **kwargs)
    return protected


def attempt_allowed():
    return current_app.extensions['auth_limiter'].allowed(request.remote_addr or 'local')


def form_response(template, errors, values, status=200):
    return render_template(template, errors=errors, values=values), status


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('main.dashboard'))
    values = {'full_name': '', 'email': ''}
    errors = {}
    if request.method == 'POST':
        values = {'full_name': request.form.get('full_name', '').strip(),
                  'email': request.form.get('email', '').strip().lower()}
        if not attempt_allowed():
            errors['form'] = 'Too many attempts. Please wait one minute and try again.'
            return form_response('auth/register.html', errors, values, 429)
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        if not 2 <= len(values['full_name']) <= 120:
            errors['full_name'] = 'Enter a name between 2 and 120 characters.'
        if not valid_email(values['email']):
            errors['email'] = 'Enter a valid email address (up to 191 characters).'
        problem = password_error(password)
        if problem:
            errors['password'] = problem
        if confirm != password:
            errors['confirm_password'] = 'Your passwords do not match.'
        if errors:
            return form_response('auth/register.html', errors, values, 400)
        if users.find_by_email(values['email']):
            errors['email'] = 'An account with this email already exists. Try logging in.'
            return form_response('auth/register.html', errors, values, 409)
        hashed = generate_password_hash(password, method='pbkdf2:sha256:600000')
        try:
            users.create_user(values['full_name'], values['email'], hashed)
        except pymysql.IntegrityError as error:
            if error.args[0] != 1062:
                raise
            errors['email'] = 'An account with this email already exists. Try logging in.'
            return form_response('auth/register.html', errors, values, 409)
        flash('Account created. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return form_response('auth/register.html', errors, values)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('main.dashboard'))
    errors = {}
    values = {'email': ''}
    next_url = safe_next(request.form.get('next') or request.args.get('next'))
    if request.method == 'POST':
        values['email'] = request.form.get('email', '').strip().lower()
        if not attempt_allowed():
            errors['form'] = 'Too many attempts. Please wait one minute and try again.'
            return render_template('auth/login.html', errors=errors, values=values,
                                   next_url=next_url), 429
        password = request.form.get('password', '')
        user = users.find_by_email(values['email']) if valid_email(values['email']) else None
        valid = False
        if user and user['is_active'] and 12 <= len(password) <= 128:
            valid = check_password_hash(user['password_hash'], password)
        if not valid:
            errors['form'] = 'Email or password is incorrect.'
            return render_template('auth/login.html', errors=errors, values=values,
                                   next_url=next_url), 401
        session.clear()
        session['user_id'] = user['id']
        session.permanent = True
        return redirect(next_url or url_for('main.dashboard'))
    return render_template('auth/login.html', errors=errors, values=values, next_url=next_url)


@bp.post('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
