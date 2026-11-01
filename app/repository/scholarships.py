"""Search, create, edit and archive catalogue records with parameterized SQL."""
from app.db import get_db


def list_all(filters=None, include_archived=False):
    filters = filters or {}
    conditions, params = [], []
    if not include_archived:
        conditions.append('is_active = 1')
    if filters.get('q'):
        term = '%' + filters['q'] + '%'
        conditions.append('(title LIKE %s OR provider LIKE %s OR field LIKE %s)')
        params.extend([term, term, term])
    for key in ('country', 'degree', 'funding'):
        if filters.get(key):
            conditions.append(f'{key} = %s')  # Fixed internal column names only.
            params.append(filters[key])
    sql = 'SELECT * FROM scholarships'
    if conditions:
        sql += ' WHERE ' + ' AND '.join(conditions)
    sql += ' ORDER BY is_active DESC, deadline IS NULL, deadline, id DESC'
    with get_db().cursor() as cursor:
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()


def find(scholarship_id):
    with get_db().cursor() as cursor:
        cursor.execute('SELECT * FROM scholarships WHERE id = %s', (scholarship_id,))
        return cursor.fetchone()


def save(data, scholarship_id=None):
    columns = ('title', 'provider', 'country', 'degree', 'field', 'funding', 'min_cgpa',
               'deadline', 'official_url', 'description', 'is_active', 'is_sample')
    values = tuple(data[key] for key in columns)
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            if scholarship_id is None:
                cursor.execute('INSERT INTO scholarships (' + ','.join(columns) + ') VALUES ('
                               + ','.join(['%s'] * len(columns)) + ')', values)
                scholarship_id = cursor.lastrowid
            else:
                cursor.execute('UPDATE scholarships SET ' + ','.join(key + '=%s' for key in columns)
                               + ' WHERE id=%s', values + (scholarship_id,))
        connection.commit()
        return scholarship_id
    except Exception:
        connection.rollback()
        raise


def toggle_active(scholarship_id):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE scholarships SET is_active = 1 - is_active WHERE id = %s',
                           (scholarship_id,))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
