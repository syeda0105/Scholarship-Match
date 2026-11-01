"""Route tests use a repository double, never a substitute production database."""
from datetime import datetime
import pytest
from app import create_app
from app.repository import users


@pytest.fixture
def accounts(monkeypatch):
    records = {}

    def create(name, email, hashed):
        user_id = len(records) + 1
        records[user_id] = dict(id=user_id, full_name=name, email=email,
                                password_hash=hashed, created_at=datetime(2026, 11, 1),
                                is_active=1)
        return user_id

    monkeypatch.setattr(users, 'create_user', create)
    monkeypatch.setattr(users, 'find_by_id', lambda key: records.get(key))
    monkeypatch.setattr(users, 'find_by_email',
                        lambda email: next((u for u in records.values() if u['email'] == email), None))
    return records


@pytest.fixture
def app(accounts):
    return create_app({'TESTING': True, 'SECRET_KEY': 'test-only-key-' * 4})


@pytest.fixture
def client(app):
    return app.test_client()
