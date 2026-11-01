import re

PASSWORD = 'A memorable passphrase!'


def token(client, path):
    html = client.get(path).get_data(as_text=True)
    return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)


def register(client, **overrides):
    data = dict(full_name='Sample Student', email='student@example.com',
                password=PASSWORD, confirm_password=PASSWORD,
                csrf_token=token(client, '/auth/register'))
    data.update(overrides)
    return client.post('/auth/register', data=data)


def login(client, **overrides):
    data = dict(email='student@example.com', password=PASSWORD,
                csrf_token=token(client, '/auth/login'))
    data.update(overrides)
    return client.post('/auth/login', data=data)
