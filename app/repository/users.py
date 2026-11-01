"""Small user repository: the only application module containing user SQL."""
from app.db import get_db


def find_by_email(email):
    with get_db().cursor() as cursor:
        cursor.execute('SELECT id, full_name, email, password_hash, created_at, is_active, role '
                       'FROM users WHERE email = %s', (email,))
        return cursor.fetchone()


def find_by_id(user_id):
    with get_db().cursor() as cursor:
        cursor.execute('SELECT id, full_name, email, created_at, is_active, role '
                       'FROM users WHERE id = %s', (user_id,))
        return cursor.fetchone()


def create_user(full_name, email, password_hash):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO users (full_name, email, password_hash) '
                           'VALUES (%s, %s, %s)', (full_name, email, password_hash))
            user_id = cursor.lastrowid
        connection.commit()
        return user_id
    except Exception:
        connection.rollback()
        raise


def promote(email):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET role='admin' WHERE email=%s AND is_active=1", (email,))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
