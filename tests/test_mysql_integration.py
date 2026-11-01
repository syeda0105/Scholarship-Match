"""Opt-in real MySQL/MariaDB check. Never defaults to the user's app database."""
import os
from pathlib import Path
import uuid
import pymysql
import pytest
from werkzeug.security import check_password_hash
from app import create_app
from .helpers import PASSWORD, register, login, token

pytestmark = pytest.mark.integration


def test_real_database_auth_and_app_restart():
    name = os.getenv('SM_TEST_MYSQL_DATABASE')
    if not name:
        pytest.skip('Set explicit SM_TEST_MYSQL_* variables for a dedicated test database.')
    if not name.endswith('_test') or not name.replace('_', '').isalnum():
        pytest.fail('Safety guard: dedicated database name must end in _test.')
    config = {
        'TESTING': True, 'SECRET_KEY': 'isolated-test-key-' * 3,
        'MYSQL_HOST': os.getenv('SM_TEST_MYSQL_HOST', '127.0.0.1'),
        'MYSQL_PORT': int(os.getenv('SM_TEST_MYSQL_PORT', '3306')),
        'MYSQL_USER': os.environ['SM_TEST_MYSQL_USER'],
        'MYSQL_PASSWORD': os.environ['SM_TEST_MYSQL_PASSWORD'],
        'MYSQL_DATABASE': name,
    }
    connection = pymysql.connect(host=config['MYSQL_HOST'], port=config['MYSQL_PORT'],
        user=config['MYSQL_USER'], password=config['MYSQL_PASSWORD'], database=name,
        cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    # Create only the users table in the explicitly named test database.
    schema = (Path(__file__).resolve().parents[1] / 'database/001_users.sql').read_text()
    table_sql = schema[schema.index('CREATE TABLE'):]
    email = f'sm-test-{uuid.uuid4().hex}@example.com'
    try:
        with connection.cursor() as cursor:
            cursor.execute(table_sql)
        app = create_app(config)
        client = app.test_client()
        assert register(client, email=email).status_code == 302
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
            row = cursor.fetchone()
        assert row and row['password_hash'] != PASSWORD
        assert check_password_hash(row['password_hash'], PASSWORD)
        assert login(client, email=email, password='Wrong password here').status_code == 401
        assert login(client, email=email).status_code == 302
        assert client.get('/welcome').status_code == 200
        assert client.post('/auth/logout', data={'csrf_token': token(client, '/welcome')}).status_code == 302
        # Build a fresh app/client: account persists beyond the application instance.
        restarted = create_app(config).test_client()
        assert login(restarted, email=email).status_code == 302
        assert restarted.get('/welcome').status_code == 200
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) AS count FROM users WHERE email=%s', (email,))
            assert cursor.fetchone()['count'] == 1
        result = app.test_cli_runner().invoke(args=['check-db'])
        assert result.exit_code == 0
        assert 'Connected to' in result.output
    finally:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM users WHERE email=%s', (email,))
        connection.close()
