# ScholarshipMatch — Authentication milestone

A standalone Python Flask + HTML/Jinja + CSS + local Bootstrap grid + vanilla
JavaScript + MySQL/PyMySQL project. **No npm, React, cloud account, AI API or paid service.**

Start with **[START_HERE.md](START_HERE.md)** for Windows setup.

## What is implemented

- Styled registration and login, password visibility toggles, responsive layout.
- A real MySQL insert on registration, salted password hash (PBKDF2-SHA256).
- Existing-account verification on login; no extra account row per login.
- Protected welcome page with account details loaded from MySQL.
- POST-only logout, session reset, CSRF, active-account checks, safe redirects.
- Parameterized SQL, explicit commit/rollback, request connection cleanup.
- Duplicate-email and form validation; clear database-unavailable errors.
- Two-hour permanent session lifetime; HttpOnly/SameSite cookies.
- Local `check-db` command, non-destructive schema, setup and test instructions.

This is **not the complete ScholarshipMatch website**. Scholarships, matching,
profile editing and administration will be implemented later. There are no fake
catalogues, admin accounts, or preview-only backends.

## Quick start (PowerShell, project root)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe setup_env.py
```

Then start WampServer's MySQL, import `database/001_users.sql` through phpMyAdmin
as an administrator, create the limited application account, and set `.env`.
See START_HERE.md for exact instructions; do **not** skip the database step.

```powershell
.\.venv\Scripts\python.exe -m flask --app wsgi check-db
.\.venv\Scripts\python.exe -m flask --app wsgi run
```

Open http://127.0.0.1:5000. Ctrl+C stops the development server.

## Structure

| File/folder | Purpose |
|---|---|
| `wsgi.py` | Entry point creating Flask |
| `app/__init__.py` | Configuration, CSRF, blueprints, safe error responses |
| `app/blueprints/auth.py` | Register/login/logout and current-user lookup |
| `app/blueprints/main.py` | Entry redirect and protected welcome page |
| `app/db.py` | MySQL connection, cleanup and check-db command |
| `app/repository/users.py` | User SELECT/INSERT queries and transactions |
| `app/security.py` | Input helpers, local redirects and development attempt limit |
| `app/templates/` | Shared layout, forms, welcome/error pages |
| `app/static/` | Offline CSS, Bootstrap grid, JS, favicon |
| `database/001_users.sql` | Only the database and users table |
| `setup_env.py`, `.env.example` | Safe local config creation/placeholders |
| `tests/` | Behavior, security, SQL binding and opt-in live DB tests |
| `docs/` | Scope, architecture, schema, routes, viva, verification |

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Without explicit test-database configuration the live integration test is skipped.
Other tests use an isolated repository double; they do not prove MySQL works.
Read `docs/TESTING.md` for recorded results and live test instructions.

## Local-development limits

- Confirm WampServer/Windows configuration on your laptop; this ZIP does not include Python or a MySQL server.
- Installation of Python packages needs internet; runtime styles/assets are local.
- The small in-process attempt limiter resets when Flask restarts and is not suitable for a multi-worker public deployment.
- No email verification/reset, admin controls, or persistent server-side session revocation in this milestone.
- Flask signed session cookies contain the user ID (not passwords), and are signed, not encrypted.
- `COOKIE_SECURE=false` is for local HTTP only. Public hosting needs HTTPS, secure cookies, a production WSGI server, durable rate limits, and deployment review.
- Password comparison is hashed; nonexistent-account responses are generic but timing equalization is not implemented.

## GitHub

Commit source, SQL, requirements, docs, tests and `.env.example`. Do not upload
`.env`, `.venv`, caches, credentials or personal database dumps. The `.gitignore`
is included. Suggested commit: `Implement Flask MySQL authentication milestone`.

## Third-party code

`bootstrap-grid.min.css` is the local Bootstrap 5.3.3 grid (MIT), distributed with
`app/static/vendor/BOOTSTRAP-LICENSE.txt`. All other visual styles are in style.css.
