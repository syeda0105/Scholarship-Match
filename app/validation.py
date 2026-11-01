"""Shared choices and small server-side form checks."""
from datetime import date
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit

DEGREES = {'undergraduate': "Bachelor's", 'masters': "Master's", 'phd': 'PhD'}
FIELDS = ('Software Engineering', 'Computer Science', 'Engineering', 'Business',
          'Medicine', 'Social Sciences', 'Other')
COUNTRIES = ('Pakistan', 'United Kingdom', 'Germany', 'Türkiye', 'United States',
             'Canada', 'Australia', 'Malaysia', 'Japan', 'Other')
FUNDING = {'fully_funded': 'Fully funded', 'partial': 'Partial funding', 'tuition_waiver': 'Tuition waiver'}


def text(form, key, errors, label, minimum=2, maximum=120):
    value = form.get(key, '').strip()
    if not minimum <= len(value) <= maximum:
        errors[key] = f'{label} must contain {minimum}–{maximum} characters.'
    return value


def choice(form, key, options, errors, label):
    value = form.get(key, '').strip()
    if value not in options:
        errors[key] = f'Select a valid {label.lower()}.'
    return value


def number(form, key, errors, label, low, high, integer=False):
    try:
        value = Decimal(form.get(key, '').strip())
        if not value.is_finite() or not low <= value <= high:
            raise ValueError
        if value != value.quantize(Decimal('1') if integer else Decimal('0.01')):
            raise ValueError
        return int(value) if integer else value
    except (InvalidOperation, ValueError):
        kind = 'a whole number' if integer else 'a number with up to 2 decimal places'
        errors[key] = f'{label} must be {kind}, from {low} to {high}.'
        return None


def web_url(value):
    try:
        parts = urlsplit(value)
        return (len(value) <= 500 and parts.scheme in ('https', 'http')
                and parts.hostname and '.' in parts.hostname
                and not parts.username and not parts.password
                and not any(char.isspace() for char in value))
    except ValueError:
        return False


def deadline(form, errors):
    raw = form.get('deadline', '').strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        errors['deadline'] = 'Enter a valid date or leave it blank.'
        return None
