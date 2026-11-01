"""Read/update only the profile of the authenticated user."""
from app.db import get_db


def find(user_id):
    with get_db().cursor() as cursor:
        cursor.execute('SELECT * FROM profiles WHERE user_id = %s', (user_id,))
        return cursor.fetchone()


def save(user_id, data):
    connection = get_db()
    values = (data['degree'], data['field'], data['cgpa'], data['nationality'],
              data['age'], data['preferred_country'], data['preferred_funding'])
    try:
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO profiles
                (user_id, degree, field, cgpa, nationality, age, preferred_country, preferred_funding)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE degree=%s, field=%s, cgpa=%s, nationality=%s,
                age=%s, preferred_country=%s, preferred_funding=%s''',
                (user_id,) + values + values)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
