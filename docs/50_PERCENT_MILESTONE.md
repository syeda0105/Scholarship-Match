# ScholarshipMatch — 50% Milestone Delivery

**Baseline archive:** `ScholarshipMatch-Auth (2).zip` (Git commit `f004cb8`)

**Milestone:** Editorial/premium interface and role-specific workspace

**Architecture retained:** Flask, Python, Jinja templates, CSS/JavaScript and MySQL

**Deferred:** DAAD and other external scholarship imports, URL extraction, scheduled source synchronisation, saved scholarships, comparison and deadline tracking.

## Delivered in this milestone

- Replaced the temporary text-mark logo with a custom navy/gold graduation-and-book mark used by the header and browser favicon.
- Reworked the public homepage around scholarship discovery, a catalogue-backed search field, real catalogue count, featured catalogue records and a three-step explanation. No fabricated global scholarship or student statistics are displayed.
- Reworked the login/registration story panel to use the new identity and a clearer academic message while retaining the existing Flask forms, validation, CSRF and authentication flow.
- Split the authenticated experience by role. Applicant navigation contains Overview, Find Scholarships, My Matches and My Profile. Administrator navigation contains Overview, Scholarships, Manage Catalogue and Add Scholarship; student-only links are not rendered for administrators.
- Redirected administrator visits to `/dashboard` to the administrator overview at `/admin`.
- Replaced the old admin catalogue landing page with an overview containing counts derived from the current scholarship records, recent catalogue records and quick actions. Moved record search and management to `/admin/catalogue`.
- Added a profile-completion prompt and progress indicator to the applicant dashboard when the academic profile is incomplete.
- Added scholarship-card elevation, refined border treatment and restrained gold hover illumination; added responsive layout rules and visible keyboard focus styling.
- Added route tests for the student profile prompt, administrator landing page/navigation and applicant denial from the admin catalogue.

## Functional requirements status

Status is assessed against the full acceptance checks in `requirements/functional-and-non-functional-requirements.md`, not merely whether a related screen exists.

| ID | Status | Evidence / remaining work |
|---|---|---|
| FR-01 | Complete | Registration, login/logout, session checks, password hashing, duplicate-email handling, CSRF and applicant-only public registration are implemented and covered by route tests. |
| FR-02 | Partial | Current profile fields and ownership are implemented; date of birth, qualification history, grading scale and test records are not yet supported. |
| FR-03 | Partial | Admin add/edit/activate/archive and official URL field exist; cycle metadata, timezone, verification date and reviewed-rule publication gate remain. |
| FR-04 | Not implemented | Eligibility rules are currently limited to fixed evaluator code; there is no admin-maintained structured rule configuration. |
| FR-05 | Partial | Degree, field and minimum-CGPA checks exist; other criteria, unknown/unresolved outcomes and grading-scale compatibility remain. |
| FR-06 | Partial | Current binary eligible/not-eligible and closed labels do not yet implement the required three-way classification and precedence rules. |
| FR-07 | Partial | Fixed weighted scoring and sorting exist; weights/ties are not admin-configurable and the full exclusion/grouping acceptance checks remain. |
| FR-08 | Partial | Criterion pass/fail explanations exist; unresolved reasons, cycle/evaluation metadata and verification details remain. |
| FR-09 | Partial | Catalogue search and country/degree/funding filters exist; field filtering and side-by-side comparison remain. |
| FR-10 | Not implemented | Persistent saved scholarships and a private applicant readiness checklist are not present. |
| FR-11 | Not implemented | Saved-scholarship deadline tracking and closed-item notifications are not present. |

**FR totals:** 1 complete, 7 partially implemented, 3 not implemented. Therefore 10 of 11 FRs still need completion or additional acceptance work.

## Non-functional requirements status

| ID | Status | Evidence / remaining verification |
|---|---|---|
| NFR-01 | Partial | Plain-language labels, field validation and status text exist; verify the full three-status eligibility experience and usability with users. |
| NFR-02 | Partial | Responsive breakpoints and compact navigation are implemented; viewport checks at 360, 768 and 1366 px have not been run in a browser. |
| NFR-03 | Not implemented | No documented 100-record performance benchmark has been run. |
| NFR-04 | Partial | Password hashing, role checks, parameterized SQL, CSRF and protected session settings exist; production HTTPS/cookie deployment verification remains. |
| NFR-05 | Partial | Environment configuration and `.env.example` exist; this delivery archive has been cleaned of `.env`, and repository/privacy review still needs to be completed on the user's GitHub copy. |
| NFR-06 | Partial | Some deterministic eligibility and boundary tests exist; unknown criteria, grading-scale, deadline-boundary and transactional cases remain. |
| NFR-07 | Partial | Request, repository and service layers are separated; eligibility rules and scoring weights are not yet maintainable as stored configuration. |
| NFR-08 | Partial | Requirements and criterion-level explanations are documented; source verification metadata, cycle and evaluation timestamp are not fully represented. |
| NFR-09 | Partial | Server-side validation, unique account handling, transactions and controlled database errors exist; full MySQL failure and data-integrity acceptance tests remain. |
| NFR-10 | Partial | Dependency files, schema scripts, `.env.example` and README setup instructions exist; a clean-environment setup and backup/restore drill have not been verified. |

**NFR totals:** 0 fully verified, 8 partially implemented, 2 not implemented. All 10 NFRs still require additional implementation and/or acceptance verification.

## Validation performed for this package

- Python source compilation: passed (`compileall`).
- Jinja template syntax parsing: passed for all 17 HTML templates.
- `git diff --check`: not used as a release gate because the supplied archive contains pre-existing line-ending/trailing-whitespace changes in the bundled `.agents` skill files.
- Full pytest suite: **71 passed, 1 skipped** on the Windows project virtual environment using `.\.venv\Scripts\python.exe -m pytest -q`. The skipped test is the opt-in MySQL integration test; this run does not verify connectivity to the user's MySQL server.
- Browser viewport and MySQL integration tests: not run in this environment.

## Next milestone

Complete the remaining requirements in priority order: structured eligibility criteria and three-way assessment, expanded profile data, catalogue comparison and saved items, deadline tracking, source verification metadata, then performance/security/response verification. External scholarship ingestion remains a later milestone after the user's research. A full admin website-content/layout editor is also not part of this delivery; the current admin overview and catalogue management are implemented, while editable homepage sections/theme controls need a separately defined scope.
