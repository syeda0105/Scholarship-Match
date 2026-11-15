# Instructions for coding assistants

- Current scope is only registration, login, protected welcome and logout with one MySQL users table. Do not implement the full website without a new request.
- Read START_HERE.md, README.md and docs/PHASE_DOCUMENTATION.md. Update these and docs/TESTING.md as behavior changes.
- There is no admin role yet. Do not pretend that future admin functionality exists.

- Stack is fixed: Flask + Jinja2 + Bootstrap/CSS3 + vanilla JS + MySQL via PyMySQL. Never add npm, React, Node, SQLite, Supabase or Firebase.
- Keep one Flask app with the factory in `app/__init__.py`; add routes to the existing blueprints.
- Routes handle HTTP only. Eligibility and scoring go in `app/services/` (no SQL, no Flask). All SQL goes in `app/repository/` with `%s` parameters, never string formatting.
- Every mutation is a POST with a CSRF token; enforce login, ownership and admin role on the server.
- Never display raw exceptions, password hashes or secrets. Secrets come only from `.env`.
- Don't invent English-test equivalences, GPA conversions, real deadlines or statistics. Sample data must be labelled fictional.
- Show the footer credit "Developed by Syeda Alysha Aly" only once; never show a roll number.
- Use colours and styles from `style.css` variables; no inline colour styles in templates.
- Update the route and traceability tables in docs/PHASE_DOCUMENTATION.md whenever routes or behaviour change. Add or update tests for every rule.
- Keep functions short and comments explanatory; this code is explained in a viva.
