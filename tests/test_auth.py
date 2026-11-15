import pytest
import pymysql
from werkzeug.security import check_password_hash
from app.repository import users
from .helpers import PASSWORD, token, register, login


def test_registration_stores_hash_and_normalized_email(client, accounts):
    response = register(client, email=' STUDENT@EXAMPLE.COM ')
    assert response.status_code == 302
    assert response.location.endswith('/auth/login')
    user = accounts[1]
    assert user['email'] == 'student@example.com'
    assert user['password_hash'] != PASSWORD
    assert user['password_hash'].startswith('pbkdf2:sha256:600000$')
    assert check_password_hash(user['password_hash'], PASSWORD)


def test_passwords_have_different_salts(client, accounts):
    register(client)
    register(client, email='other@example.com')
    assert accounts[1]['password_hash'] != accounts[2]['password_hash']


@pytest.mark.parametrize('changes', [
    {'full_name': 'A'}, {'full_name': 'A' * 121}, {'email': 'bad'},
    {'email': '..bad@example.com'}, {'password': 'short', 'confirm_password': 'short'},
    {'password': 'x' * 129, 'confirm_password': 'x' * 129}, {'confirm_password': 'different'},
])
def test_invalid_registration_does_not_insert(client, accounts, changes):
    assert register(client, **changes).status_code == 400
    assert accounts == {}


def test_duplicate_registration_rejected(client, accounts):
    register(client)
    assert register(client, email='STUDENT@example.com').status_code == 409
    assert len(accounts) == 1


def test_successful_login_does_not_create_another_row(client, accounts):
    register(client)
    response = login(client)
    assert response.status_code == 302
    assert response.location.endswith('/dashboard')
    welcome = client.get('/dashboard')
    assert welcome.status_code == 200
    assert b'Sample Student' in welcome.data
    assert b'Hello, Sample' in welcome.data
    assert b'pbkdf2' not in welcome.data
    assert len(accounts) == 1


@pytest.mark.parametrize('changes', [{'password': 'Wrong long password'}, {'email': 'nobody@example.com'}, {'email': 'invalid'}])
def test_bad_credentials_rejected(client, changes):
    register(client)
    assert login(client, **changes).status_code == 401
    assert client.get('/dashboard').status_code == 302


def test_inactive_user_rejected_and_existing_session_invalidated(client, accounts):
    register(client)
    login(client)
    accounts[1]['is_active'] = 0
    assert client.get('/dashboard').status_code == 302
    assert login(client).status_code == 401


def test_welcome_requires_login(client):
    assert client.get('/dashboard').location.endswith('/auth/login?next=/dashboard')


def test_logout_requires_post_and_csrf(client):
    register(client)
    login(client)
    assert client.get('/auth/logout').status_code == 405
    assert client.post('/auth/logout').status_code == 400
    csrf = token(client, '/dashboard')
    assert client.post('/auth/logout', data={'csrf_token': csrf}).status_code == 302
    assert client.get('/dashboard').status_code == 302


@pytest.mark.parametrize('path', ['/auth/register', '/auth/login'])
def test_csrf_is_enforced(client, path):
    assert client.post(path, data={}).status_code == 400


def test_csrf_rotates_on_login(client):
    register(client)
    before = token(client, '/auth/login')
    login(client)
    assert token(client, '/dashboard') != before


@pytest.mark.parametrize('target', ['https://example.com', '//example.com', '/\\example.com', '/%2fexample.com'])
def test_external_redirect_rejected(client, target):
    register(client)
    assert login(client, next=target).location.endswith('/dashboard')


def test_deleted_account_cannot_keep_session(client, accounts):
    register(client)
    login(client)
    accounts.clear()
    assert client.get('/dashboard').status_code == 302


def test_rate_limit(client):
    for _ in range(10):
        assert login(client).status_code == 401
    assert login(client).status_code == 429


def test_database_unavailable_is_honest(client, monkeypatch):
    def unavailable(email):
        raise pymysql.OperationalError(2003, 'private credentials must not be shown')
    monkeypatch.setattr(users, 'find_by_email', unavailable)
    response = login(client)
    assert response.status_code == 503
    assert b'Database unavailable' in response.data
    assert b'private credentials' not in response.data


@pytest.mark.parametrize('name', ['###', '@@@', '****', '12345', '111111', '123ABC', '<script>alert(1)</script>', '- -', "'Ali", 'Ali-'])
def test_invalid_names_rejected(client, accounts, name):
    assert register(client, full_name=name).status_code == 400
    assert accounts == {}


@pytest.mark.parametrize('name', ['Alysha', 'Alysha Khan', 'Muhammad Ali', 'Mary Jane Watson', "O'Connor", 'Anne-Marie', 'José Ñandú', 'عائشہ فاطمہ'])
def test_valid_names_accepted(client, accounts, name):
    assert register(client, full_name=name).status_code == 302
    assert accounts[1]['full_name'] == name


def test_name_whitespace_is_normalized(client, accounts):
    register(client, full_name='  Alysha    Khan  ')
    assert accounts[1]['full_name'] == 'Alysha Khan'
