from pathlib import Path
import pytest
from app import create_app
from setup_env import create_env


def test_setup_creates_secret_without_overwriting(tmp_path):
    (tmp_path / '.env.example').write_text('SECRET_KEY=REPLACE_WITH_RANDOM_SECRET\n')
    assert create_env(tmp_path)
    original = (tmp_path / '.env').read_text()
    assert len(original.strip().split('=')[1]) == 64
    assert not create_env(tmp_path)
    assert original == (tmp_path / '.env').read_text()


@pytest.mark.parametrize('key', ['', 'short', 'REPLACE_' + 'x' * 50])
def test_missing_or_placeholder_secret_rejected(key):
    with pytest.raises(RuntimeError):
        create_app({'SECRET_KEY': key})


def test_pages_and_local_assets_load_without_mysql(client):
    assert client.get('/').status_code == 302
    for path in ['/auth/login', '/auth/register', '/static/css/style.css',
                 '/static/css/bootstrap-grid.min.css', '/static/js/main.js', '/static/favicon.svg']:
        assert client.get(path).status_code == 200
    html = client.get('/auth/login').get_data(as_text=True)
    assert html.count('Developed by Syeda Alysha Aly') == 1
    assert 'https://' not in html
    assert '/static/css/style.css' in html


def test_error_handlers(client, app):
    from flask import abort
    @app.get('/test-403')
    def forbidden():
        abort(403)
    @app.get('/test-500')
    def failure():
        raise RuntimeError('hidden internal detail')
    app.config['PROPAGATE_EXCEPTIONS'] = False
    assert client.get('/missing').status_code == 404
    assert client.get('/test-403').status_code == 403
    response = client.get('/test-500')
    assert response.status_code == 500
    assert b'hidden internal detail' not in response.data


def test_check_db_fails_with_nonzero_exit(app, monkeypatch):
    import pymysql
    from app import db
    def fail():
        raise pymysql.OperationalError(2003, 'not connected')
    monkeypatch.setattr(db, 'get_db', fail)
    result = app.test_cli_runner().invoke(args=['check-db'])
    assert result.exit_code != 0
    assert 'check failed' in result.output


def test_schema_is_nondestructive_and_does_not_seed_passwords():
    sql = (Path(__file__).resolve().parents[1] / 'database/001_users.sql').read_text()
    assert 'DROP TABLE' not in sql and 'INSERT INTO users' not in sql
    assert 'email VARCHAR(191) NOT NULL UNIQUE' in sql
