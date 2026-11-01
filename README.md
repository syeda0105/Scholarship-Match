# ScholarshipMatch

A scholarship discovery website developed for the Software Construction
& Development course.

## Technology

- Backend: Python and Flask
- Frontend: HTML, Jinja templates, CSS, Bootstrap grid and vanilla JavaScript
- Database: MySQL
- Database connectivity: PyMySQL

## Implemented Features

- User registration, login and logout
- Password hashing and input validation
- Student dashboard
- Academic profile creation and editing with MySQL persistence
- Scholarship catalogue with search and filters
- Individual scholarship details
- Administrator-only scholarship creation, editing and visibility management
- Responsive interfaces for desktop and mobile

## Database

The database is named `scholarshipmatch_auth`.

| Table | Purpose |
|---|---|
| users | User accounts, password hashes and roles |
| profiles | Academic details and study preferences |
| scholarships | Scholarship information and catalogue visibility |

Registration creates a user record. Login verifies the existing account.
Saving or editing an academic profile updates the authenticated user's data.

## Local Setup — Windows

Requirements: Python, VS Code, and a running MySQL service such as
WampServer's MySQL.

### First installation only

Run these commands from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup_env.py
```

Using phpMyAdmin with a database administrator account, import:

1. `database/001_users.sql`
2. `database/002_upgrade.sql`
3. `database/003_demo_data.sql` — optional fictional demonstration data

Create an application MySQL account with SELECT, INSERT, UPDATE and DELETE
permissions on `scholarshipmatch_auth.*`.

Set the MYSQL_* values in your local `.env` to match your database credentials.
Keep the generated SECRET_KEY private. Use COOKIE_SECURE=false for local HTTP.

### Updating the earlier authentication version

Back up the project and database first.

Keep the existing `.env`, `.venv`, database and registered accounts.
Import only `database/002_upgrade.sql`; optionally import the demonstration data.
Do not repeat the initial installation steps.

### Start the application

Keep MySQL running, then execute:

```powershell
.\.venv\Scripts\python.exe -m flask --app wsgi check-db
.\.venv\Scripts\python.exe -m flask --app wsgi run
```

Open http://127.0.0.1:5000.

Public registration creates student accounts. Administrative actions require
an account with the admin role.

## Project Structure

- `app/blueprints/` — Flask routes and access checks
- `app/repository/` — Database queries
- `app/templates/` — HTML/Jinja pages
- `app/static/` — CSS, JavaScript and visual assets
- `app/validation.py` — Shared input validation
- `database/` — Schema, upgrade and optional demonstration SQL
- `tests/` — Automated tests
- `wsgi.py` — Application entry point
- `setup_env.py` — Initial local configuration

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Live database tests require their separate test configuration.
Never point database integration tests at the application's existing database.

## Security and Repository Rules

- Passwords are stored as hashes.
- POST forms use CSRF protection.
- Database queries use bound parameters.
- Administrative routes enforce role checks.
- Never commit `.env`, `.venv`, credentials or personal database exports.
- `.env.example` contains configuration placeholders only.

## Current Scope

Eligibility calculation, recommendation ranking, comparison, application
submission and deadline reminders are planned for later development.

The optional demonstration scholarships are fictional and are labelled
as samples. They are not verified scholarship opportunities.

This application currently runs locally. Uploading its source to GitHub
does not deploy the Flask server or MySQL database.