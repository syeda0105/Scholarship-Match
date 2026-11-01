"""Simple form validation, safe redirects, and a local-development attempt limit."""
from collections import defaultdict, deque
from threading import Lock
from time import monotonic
from urllib.parse import urlsplit
import re

EMAIL = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+")


def valid_email(email):
    if len(email) > 191 or not EMAIL.fullmatch(email):
        return False
    local = email.split('@')[0]
    return len(local) <= 64 and not local.startswith('.') and not local.endswith('.') and '..' not in local


def password_error(password):
    if not 12 <= len(password) <= 128:
        return 'Use between 12 and 128 characters.'
    if not (any(c.isupper() for c in password) and any(c.islower() for c in password)
            and any(c.isdigit() for c in password) and any(not c.isalnum() and not c.isspace() for c in password)):
        return 'Include an uppercase letter, a lowercase letter, a number and a symbol.'
    return None


def safe_next(value):
    """Allow local paths only, including after URL decoding by the browser."""
    if not value or not value.startswith('/') or value.startswith('//'):
        return None
    if '\\' in value or '%' in value or any(ord(char) < 32 for char in value):
        return None
    parsed = urlsplit(value)
    return value if not parsed.scheme and not parsed.netloc else None


class AttemptLimiter:
    """Ten auth POST attempts per IP per minute. Resets on server restart."""
    def __init__(self):
        self.attempts = defaultdict(deque)
        self.lock = Lock()

    def allowed(self, address):
        now = monotonic()
        with self.lock:
            # Expire idle entries so the development limiter stays bounded.
            for key in list(self.attempts):
                if not self.attempts[key] or self.attempts[key][-1] < now - 60:
                    del self.attempts[key]
            queue = self.attempts[address]
            while queue and queue[0] < now - 60:
                queue.popleft()
            if len(queue) >= 10:
                return False
            queue.append(now)
            return True
