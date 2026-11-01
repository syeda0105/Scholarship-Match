"""One MySQL connection per request; PyMySQL sends real SQL to MySQL."""
import click
import pymysql
from pymysql.cursors import DictCursor
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        config = current_app.config
        g.db = pymysql.connect(
            host=config['MYSQL_HOST'], port=config['MYSQL_PORT'],
            user=config['MYSQL_USER'], password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE'], charset='utf8mb4',
            cursorclass=DictCursor, autocommit=False,
            connect_timeout=5, read_timeout=5, write_timeout=5,
        )
    return g.db


def close_db(error=None):
    connection = g.pop('db', None)
    if connection:
        connection.close()


@click.command('check-db')
@with_appcontext
def check_db():
    """Verify an actual connection and that the users table is readable."""
    try:
        with get_db().cursor() as cursor:
            cursor.execute('SELECT DATABASE() AS name')
            database = cursor.fetchone()['name']
            cursor.execute('SELECT COUNT(*) AS count FROM users')
            count = cursor.fetchone()['count']
            cursor.execute('SELECT role FROM users LIMIT 1')
            cursor.execute('SELECT user_id FROM profiles LIMIT 1')
            cursor.execute('SELECT id FROM scholarships LIMIT 1')
        click.echo(f'Connected to {database}. users table readable: {count} account(s).')
    except pymysql.MySQLError:
        raise click.ClickException('Database/schema check failed. Check .env and the MySQL service; '
                                   'import database/002_upgrade.sql as described in UPGRADE.md.')


@click.command('make-admin')
@click.option('--email', prompt='Existing registered email')
@with_appcontext
def make_admin(email):
    """Promote an existing local account; no public route can create admins."""
    from .repository import users
    user = users.find_by_email(email.strip().lower())
    if not user or not user['is_active']:
        raise click.ClickException('Register an active account with that email first.')
    if click.confirm(f"Grant administrator access to {user['email']}?"):
        users.promote(user['email'])
        click.echo('Administrator role saved. Log in to open scholarship management.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(check_db)
    app.cli.add_command(make_admin)
