"""Create the small Flask application and connect its components."""
from datetime import timedelta
from pathlib import Path
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect, CSRFError
import pymysql

from . import db

csrf = CSRFProtect()


def create_app(test_config=None):
    root = Path(__file__).resolve().parent.parent
    load_dotenv(root / '.env')
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', ''),
        MYSQL_HOST=os.getenv('MYSQL_HOST', '127.0.0.1'),
        MYSQL_PORT=int(os.getenv('MYSQL_PORT', '3306')),
        MYSQL_DATABASE=os.getenv('MYSQL_DATABASE', 'scholarshipmatch_auth'),
        MYSQL_USER=os.getenv('MYSQL_USER', 'scholarshipmatch_app'),
        MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD', ''),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=os.getenv('COOKIE_SECURE', 'false').lower() == 'true',
        PERMANENT_SESSION_LIFETIME=timedelta(hours=2),
        MAX_CONTENT_LENGTH=32 * 1024,
    )
    if test_config:
        app.config.update(test_config)
    secret = app.config['SECRET_KEY']
    if not app.testing and (len(secret) < 32 or 'REPLACE_' in secret.upper()
                            or secret.lower() in {'change-me', 'secret' * 8}):
        raise RuntimeError('Run setup_env.py to create a random SECRET_KEY in .env.')

    csrf.init_app(app)
    db.init_app(app)
    from .security import AttemptLimiter
    app.extensions['auth_limiter'] = AttemptLimiter()
    from .blueprints.auth import bp
    from .blueprints.main import bp as main_bp
    app.register_blueprint(bp)
    app.register_blueprint(main_bp)
    from .blueprints.profile import bp as profile_bp
    from .blueprints.scholarships import bp as scholarships_bp
    from .blueprints.admin import bp as admin_bp
    app.register_blueprint(profile_bp)
    app.register_blueprint(scholarships_bp)
    app.register_blueprint(admin_bp)
    from .validation import DEGREES, FIELDS, COUNTRIES, FUNDING

    @app.context_processor
    def form_choices():
        return dict(degrees=DEGREES, fields=FIELDS, countries=COUNTRIES, funding=FUNDING)

    @app.errorhandler(CSRFError)
    def bad_csrf(error):
        return render_template('errors/error.html', title='Your form has expired',
                               message='Reload the page, then submit the form again.'), 400

    @app.errorhandler(pymysql.MySQLError)
    def database_error(error):
        # Keep connection strings and raw SQL out of browser responses.
        app.logger.error('MySQL operation failed (%s).', type(error).__name__)
        return render_template('errors/error.html', title='Database unavailable',
                               message='Please try again shortly. For local setup, check '
                               'that MySQL is running and your .env is configured.'), 503

    @app.errorhandler(404)
    @app.errorhandler(403)
    @app.errorhandler(405)
    @app.errorhandler(413)
    @app.errorhandler(500)
    def error_page(error):
        code = getattr(error, 'code', 500)
        messages = {404: ('Page not found', 'This address does not lead to a page.'),
                    403: ('Access denied', 'You do not have access to this page.'),
                    405: ('Action not allowed', 'Please use the buttons on the website.'),
                    413: ('Request too large', 'Please submit a smaller form.'),
                    500: ('Something went wrong', 'Please try again shortly.')}
        title, message = messages.get(code, messages[500])
        return render_template('errors/error.html', title=title, message=message), code

    @app.after_request
    def response_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'same-origin'
        if not request.path.startswith('/static/'):
            response.headers['Cache-Control'] = 'no-store'
        return response

    return app
