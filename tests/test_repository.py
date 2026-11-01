from unittest.mock import MagicMock
import pytest
from app.repository import users


def test_sql_parameter_binding_and_commit(monkeypatch):
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.lastrowid = 12
    monkeypatch.setattr(users, 'get_db', lambda: connection)
    hostile_email = "x' OR 1=1 --@example.com"
    users.find_by_email(hostile_email)
    sql, params = cursor.execute.call_args.args
    assert hostile_email not in sql
    assert params == (hostile_email,)
    assert users.create_user('Student', 's@example.com', 'hashed') == 12
    connection.commit.assert_called_once()


def test_write_failure_rolls_back(monkeypatch):
    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value.execute.side_effect = RuntimeError('write failed')
    monkeypatch.setattr(users, 'get_db', lambda: connection)
    with pytest.raises(RuntimeError):
        users.create_user('Student', 's@example.com', 'hashed')
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
