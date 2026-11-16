# Authentication phase documentation

## Requirements and acceptance

| ID | Requirement | Verification |
|---|---|---|
| AUTH-01 | Registration stores exactly one MySQL row | Integration test + phpMyAdmin |
| AUTH-02 | Validate name/email/password/confirmation and duplicates | Route tests |
| AUTH-03 | Salted hash, no plaintext password | Hash verification and row inspection |
| AUTH-04 | Correct login succeeds, wrong/inactive login fails | Route + integration tests |
| AUTH-05 | Welcome is authenticated and shows current account only | Session/access tests |
| AUTH-06 | Logout is POST-only, token protected | CSRF tests |
| AUTH-07 | Account remains after app restart | Integration test + manual restart |
| AUTH-08 | Responsive styled forms with local assets | Browser checks |
| AUTH-09 | Secrets external; errors do not reveal DB details | Config/error tests |
| UI-01 | Dashboard routes and administrator navigation are role-specific | Route tests |
| UI-02 | Applicant dashboard prompts for an incomplete academic profile | Route tests |

The AUTH requirements describe the authentication phase. UI-01 and UI-02 trace the
later dashboard and administrator-navigation behavior covered by this delivery.

## Architecture and design

One Flask application: HTTP routes → user repository → PyMySQL → MySQL.
Jinja templates render the forms and account; local CSS/Bootstrap grid and optional
JS control appearance/password visibility. No SQL in templates or JavaScript.

Application factory configures dependencies. Blueprints group main/auth routes.
Shared base layout prevents duplicate CSS links and repeated navigation.
Repository separates user persistence. These are structural choices, not claims
that every design pattern has been implemented. Future pattern choices should
match the final class diagram and be justified by an actual need.

## Database

`scholarshipmatch_auth.users` uses InnoDB and utf8mb4:

| Column | Meaning |
|---|---|
| id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY | Stable account identifier |
| full_name VARCHAR(120) NOT NULL | Display name |
| email VARCHAR(191) NOT NULL UNIQUE | Normalized account email |
| password_hash VARCHAR(255) NOT NULL | Werkzeug PBKDF2 salted hash |
| created_at DATETIME DEFAULT CURRENT_TIMESTAMP | Creation time on DB server |
| is_active TINYINT(1) DEFAULT 1 | Allows inactive account rejection |

No seed accounts and no admin roles in this phase. Timestamps display the stored
database date; timezone normalization can be added when deadlines exist.

## Route/API contract

Server-rendered HTML, not a separate JSON API:

| Method | Path | Input | Result |
|---|---|---|---|
| GET | / | — | Public scholarship discovery homepage |
| GET | /auth/register | — | Registration form |
| POST | /auth/register | full_name, email, password, confirm_password, csrf_token | Insert + 302 login; 400 invalid; 409 duplicate; 429 limit; 503 DB failure |
| GET | /auth/login | optional next | Login form |
| POST | /auth/login | email, password, csrf_token, optional next | 302 welcome/local destination; 401 invalid; 429 limit; 503 DB failure |
| GET | /welcome | signed session cookie | Redirect to dashboard or 302 login |
| GET | /dashboard | signed session cookie | Applicant dashboard or redirect admin to `/admin` |
| GET | /admin | admin session | Administrator overview; non-admin receives 403 |
| GET | /admin/catalogue | admin session, optional `q` | Searchable scholarship management list |
| GET, POST | /admin/scholarships/new | admin session; scholarship fields on POST | Create form/save; POST requires CSRF |
| GET, POST | /admin/scholarships/<id>/edit | admin session; scholarship fields on POST | Edit form/save; POST requires CSRF |
| POST | /admin/scholarships/<id>/toggle | admin session, csrf_token | Change visibility and redirect to catalogue |
| POST | /auth/logout | csrf_token | Clear session + 302 login |
| GET | /auth/logout | — | 405 |
| GET | /static/... | — | Local CSS/JS/assets |

CSRF failures return 400. Sessions expire after two hours. After login the session
is cleared/re-established; private pages use `Cache-Control: no-store`. Active
user identity is reloaded server-side. Account details are escaped by Jinja.
Administrator access is checked on the server for every management route.

## Integration/MCP

No MCP service is needed. PyMySQL is the database driver; it is not MCP.
The application does not require an AI account, external API, or paid platform.

## Development workflow

Keep this project folder as the base for later phases. Commit this authentication
milestone to Git before adding scholarship features. Do not merge old React/Node
folders or `.venv` files into this source. Verify the login demo locally first.

## Eligibility recommendations phase

The authenticated `/recommendations` page compares a saved student profile with active scholarship records. The current schema supports three mandatory checks only: target degree, field of study (including `All fields`), and minimum CGPA. Their match-score weights are 25%, 25%, and 50%. Country and funding selections are displayed as preferences; they are not treated as mandatory eligibility rules. The page warns that the result is preliminary and that official scholarship rules may include additional criteria.

Implementation:
- `app/services/eligibility_strategies.py`: Strategy interface, concrete degree/field/CGPA strategies, and Simple Factory.
- `app/services/recommendation_facade.py`: Facade that orchestrates checks and uses `ThreadPoolExecutor` to assess multiple scholarship records concurrently.
- `app/blueprints/recommendations.py` and `app/templates/recommendations.html`: authenticated route and results UI.

Thread-safety boundary: the route loads profile and scholarship rows through the normal request-scoped repositories first. Only detached Python dictionaries/values are passed to worker threads. Workers do not use Flask `g`, sessions, or the request's MySQL connection. This avoids sharing a PyMySQL connection across threads.

Run the automated checks with `pytest -q`. The MySQL integration test is opt-in and must use a dedicated database whose name ends in `_test`.
