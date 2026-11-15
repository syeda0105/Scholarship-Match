# Verification report — 1 November 2026

## Automated behavior checks

Executed in an isolated Linux environment with Python 3.12, Flask 3.1.3,
Flask-WTF 1.2.2, PyMySQL 1.2.3, Werkzeug 3.1.9 and pytest 9.1.1.

Command: `python -m pytest -q`

- Without explicit database test configuration: **38 passed, 1 skipped**.
- With an isolated real MariaDB 10.11.14 database and explicit test variables:
  **39 passed** (including the real database integration test).

The integration test creates a user with a unique test email, reads the real SQL
row, verifies the salted password hash, checks bad/correct login, welcome/logout,
creates a fresh Flask app/client and logs in again, confirms only one account row,
checks the real check-db command, and deletes only its own test account.

Unit/route tests use a repository double and are not database evidence. Repository
mock tests verify parameter binding, commit and rollback. They are labelled
separately from the live integration test.

Other checks: Python compileall and JavaScript syntax check passed.

## Browser and visual checks

Headless Chromium browser checks completed against a real local Flask server:

- Desktop login/register visually inspected; mobile registration visually inspected.
- Layout widths 320, 390, 768 and 1440 px checked: no horizontal overflow.
- Password show/hide interaction passed. No failed CSS/JS HTTP requests.
- A separate browser flow against real MariaDB passed registration, wrong-password
  rejection, correct login, welcome, logout and protected-page redirect.
- Flask was stopped and restarted as a separate process; the same account logged
  in again. The database still contained exactly one account and its hash.
- That browser flow used a database account with SELECT/INSERT/UPDATE/DELETE only,
  matching the proposed runtime permissions. Schema import was done separately.
- Welcome page desktop/mobile screenshots were inspected for layout.

Review browser: Chrome headless shell 156.0.8078.79. These checks used fictional
data only. All fonts, styles and scripts came from local project assets.

## Run the ordinary tests on Windows

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Expected default outcome: 38 passed and 1 integration test skipped. A skip means
the real MySQL test has not been requested, not that connectivity has passed.

## Opt-in real MySQL test

Use a **separate** database, e.g. `scholarshipmatch_auth_test`, created through
phpMyAdmin. Create a dedicated test-only user with CREATE, SELECT, INSERT, UPDATE,
DELETE on that database only. The test creates its users table if absent and
cleans up its own randomly named account; it does not drop tables or truncate data.
Do not use the website's real database as the test database.

PowerShell, with values for your local test account:

```powershell
$env:SM_TEST_MYSQL_DATABASE = "scholarshipmatch_auth_test"
$env:SM_TEST_MYSQL_HOST = "127.0.0.1"
$env:SM_TEST_MYSQL_PORT = "3306"
$env:SM_TEST_MYSQL_USER = "YOUR_TEST_DATABASE_USER"
$testPassword = Read-Host "Test database password" -AsSecureString
$env:SM_TEST_MYSQL_PASSWORD = [System.Net.NetworkCredential]::new("", $testPassword).Password
.\.venv\Scripts\python.exe -m pytest -q -m integration
Remove-Item Env:SM_TEST_MYSQL_PASSWORD
Remove-Variable testPassword
```

The database name must end in `_test`, otherwise the test refuses to run. These
variables override test connectivity only; normal website configuration remains
in `.env`. Tests never fall back to the app database when test config is missing.

## Remaining environment checks

The user's specific Windows/WampServer MySQL installation, port, account-host
matching and credentials must be verified locally using START_HERE.md. MariaDB
is a real relational server using the MySQL protocol, but it is not a claim that
Oracle MySQL 8 or every WampServer release has been executed in this environment.
No public production deployment was performed or claimed.
