# ScholarshipMatch — Use Cases

| Field | Value |
| --- | --- |
| Author | Syeda Alysha Aly |
| Registration number | F24-BSSE-110 |
| Course | Software Construction & Development |
| Stage | 3 — Use Case Modelling |
| Version / Date | 0.1 / 20 October 2026 |
| Status | Design draft; describes intended behavior, not completed implementation |

## 1. Scope and Inputs

This model covers the semester application for undergraduate, master's and PhD opportunities. It follows [the requirements baseline](requirements-baseline.md) and [the refined FRs/NFRs](functional-and-non-functional-requirements.md). The refined requirements take precedence for the Python/Flask technology decision and support for all three degree levels.

## 2. Use Case Diagram

![ScholarshipMatch Use Case Diagram](diagrams/use-case-diagram.png)

[Editable Draw.io diagram](diagrams/use-case-diagram.drawio)

Open the `.drawio` file in diagrams.net to edit it. Solid lines represent actor associations; dashed arrows marked «include» point from a calling use case to required reused behavior. Positions and lines can be adjusted without changing the underlying use cases.

## 3. Modelling Decisions

- Applicant and Administrator are separate roles. Public registration cannot create administrators.
- Login is a precondition for protected use cases, not an included operation repeated on every action. For this baseline, catalogue use is authenticated; anonymous browsing is not required.
- UC-06 and UC-07 include UC-14. UC-14 includes UC-15. The included behaviors are not additional user roles or standalone screens.
- The database and Flask are internal implementation details, not external actors. Scholarship providers are external information sources; no automatic provider integration exists in the initial version.
- Administrative add/edit/activate/archive operations are grouped under Manage Scholarship Records to keep the overview readable; rule configuration is a separate use case.
- No «extend» relationship is needed for the defined flows. Optional and error paths are documented below.
- Expiry is an opportunity status, separate from an applicant's academic eligibility. Scheduled import, email/SMS notifications, document uploads and provider application submission remain outside initial scope.

## 4. Use Case Catalogue

| ID | Use case | Actor / invocation | Related FRs |
| --- | --- | --- | --- |
| UC-01 | Register | Applicant | FR-01 |
| UC-02 | Log In | Applicant or Administrator | FR-01 |
| UC-03 | Log Out | Applicant or Administrator | FR-01 |
| UC-04 | Manage Profile | Applicant | FR-02 |
| UC-05 | Browse / Filter Scholarships | Applicant | FR-09 |
| UC-06 | Check Eligibility | Applicant | FR-05, FR-06, FR-08 |
| UC-07 | View Recommendations | Applicant | FR-07, FR-08 |
| UC-08 | Compare Scholarships | Applicant | FR-09 |
| UC-09 | Manage Saved Scholarships | Applicant | FR-10 |
| UC-10 | Update Requirement Checklist | Applicant | FR-10 |
| UC-11 | View Saved Deadlines | Applicant | FR-11 |
| UC-12 | Manage Scholarship Records | Administrator | FR-03 |
| UC-13 | Manage Eligibility Rules | Administrator | FR-04 |
| UC-14 | Evaluate Mandatory Criteria | Included system behavior; no independent actor | FR-05, FR-06 |
| UC-15 | Generate Eligibility Explanation | Included system behavior; no independent actor | FR-08 |

## 5. Use Case Descriptions

### UC-01 — Register

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-01 |
| Preconditions | The applicant is not logged in. |
| Main success flow | Enter name, email and password; validate input and email uniqueness; store a salted password hash; create an applicant account. |
| Alternative / exception flow | Reject invalid input or duplicate email. Ignore or reject any attempted administrator role assignment. |
| Postconditions | A new applicant account exists; no administrator privileges are granted. |

### UC-02 — Log In

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant or Administrator |
| Requirement links | FR-01 |
| Preconditions | An account exists and the user is not logged in. |
| Main success flow | Enter credentials; verify the stored password hash; create an authenticated session; show the appropriate dashboard. |
| Alternative / exception flow | Reject invalid credentials without exposing sensitive account details. A database failure produces a controlled error. |
| Postconditions | An authenticated session exists with the stored account role. |

### UC-03 — Log Out

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant or Administrator |
| Requirement links | FR-01 |
| Preconditions | The user is logged in. |
| Main success flow | Request logout; invalidate the authenticated session; return to a public page. |
| Alternative / exception flow | If the session has already expired, return to the public/login page. |
| Postconditions | Protected actions require login again. |

### UC-04 — Manage Profile

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-02 |
| Preconditions | The applicant is logged in. |
| Main success flow | Open the profile; enter or edit qualifications, target degree, academic results and scale, field, nationality, date of birth, relevant tests and preferences; validate and save; show confirmation. |
| Alternative / exception flow | Reject invalid values. Allow explicitly unknown information where supported. Reject access to another account. |
| Postconditions | The valid profile is stored and available to subsequent assessments. |

### UC-05 — Browse / Filter Scholarships

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-09 |
| Preconditions | The applicant is logged in; scholarship records may be available. |
| Main success flow | Open the catalogue; select degree, country, funding or field filters; display matching opportunities and open a detail page with source information. |
| Alternative / exception flow | Display an empty-result message when no records match. Indicate closed records clearly if shown. |
| Postconditions | The applicant can inspect matching recorded opportunities; no profile data is changed. |

### UC-06 — Check Eligibility

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-05, FR-06, FR-08 |
| Preconditions | The applicant is logged in and has a profile; a published scholarship with a reviewed rule set is selected. |
| Main success flow | Request assessment; include UC-14 Evaluate Mandatory Criteria; display the status, rule outcomes and explanation with the source and verification date. |
| Alternative / exception flow | Unknown inputs or unsupported mandatory conditions follow unresolved-check rules. A confirmed mandatory failure takes precedence. A closed opportunity is identified separately from academic eligibility. |
| Postconditions | The applicant sees an assessment against the recorded criteria, not a selection guarantee. |

### UC-07 — View Recommendations

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-07, FR-08 |
| Preconditions | The applicant is logged in, has a profile, and a scoring configuration is defined. |
| Main success flow | Request recommendations; select open published opportunities; include UC-14 for each candidate; exclude ineligible opportunities; calculate preference-based scores; display ranking, clear eligibility labels and explanations. |
| Alternative / exception flow | Show no-results or missing-information guidance as appropriate. Identify potentially eligible opportunities clearly; final grouping and score details remain pending. |
| Postconditions | Recommendations are displayed without preference scores overriding mandatory failures. |

### UC-08 — Compare Scholarships

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-09 |
| Preconditions | The applicant is logged in and at least two opportunities are available for selection. |
| Main success flow | Select two opportunities; request comparison; display consistent fields side by side, including degree, funding, country, deadline and recorded requirements. |
| Alternative / exception flow | Ask for a second selection if only one is selected. Clearly label unavailable data. The upper comparison limit is a UI decision. |
| Postconditions | The applicant can compare the selected records; selection does not imply eligibility. |

### UC-09 — Manage Saved Scholarships

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-10 |
| Preconditions | The applicant is logged in and the selected opportunity exists. |
| Main success flow | Save an opportunity; create a unique applicant-opportunity association; display saved items. When requested, remove the saved association. |
| Alternative / exception flow | Do not create duplicate saved items. Reject access to another applicant's saved list. |
| Postconditions | The applicant's saved list reflects the operation. |

### UC-10 — Update Requirement Checklist

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-10 |
| Preconditions | The applicant is logged in and has a saved opportunity with checklist items. |
| Main success flow | Open the checklist; mark a requirement ready or not ready; validate ownership; save and display the updated state. |
| Alternative / exception flow | Report unavailable items or a save failure without falsely confirming success. |
| Postconditions | Applicant-reported readiness is stored; no documents are uploaded and eligibility is not automatically overridden. |

### UC-11 — View Saved Deadlines

| Field | Description |
| --- | --- |
| Actor / invocation | Applicant |
| Requirement links | FR-11 |
| Preconditions | The applicant is logged in. |
| Main success flow | Open saved deadlines; read the applicant's saved opportunities; list upcoming cutoffs chronologically with timezones; identify closed opportunities separately. |
| Alternative / exception flow | Display a clear empty state when no saved deadlines exist. Do not reopen a scholarship automatically for another cycle. |
| Postconditions | The applicant sees recorded deadlines and current open/closed information. |

### UC-12 — Manage Scholarship Records

| Field | Description |
| --- | --- |
| Actor / invocation | Administrator |
| Requirement links | FR-03 |
| Preconditions | The administrator is logged in with administrative authorization. |
| Main success flow | Open management; add or edit a record with source URL, application cycle, deadline/timezone and verification date; validate and save; activate a reviewed record or archive it when requested. |
| Alternative / exception flow | Reject unauthorized requests and invalid/missing publication metadata. An unreviewed rule set prevents publication. A failed save does not leave a partially updated record. |
| Postconditions | Scholarship records reflect the authorized operation; archived/expired records are excluded from open recommendations. |

### UC-13 — Manage Eligibility Rules

| Field | Description |
| --- | --- |
| Actor / invocation | Administrator |
| Requirement links | FR-04 |
| Preconditions | The administrator is logged in; the scholarship record exists. |
| Main success flow | Open its rules; define applicable mandatory criteria and thresholds/scales; distinguish unrestricted conditions from unknown ones; record unsupported requirements; validate and save the reviewed configuration. |
| Alternative / exception flow | Reject invalid thresholds/configuration. Record an unsupported interpretation as requiring verification instead of inventing a rule or conversion. |
| Postconditions | The stored rule configuration is available to subsequent evaluations. |

### UC-14 — Evaluate Mandatory Criteria

| Field | Description |
| --- | --- |
| Actor / invocation | Included system behavior; no independent actor |
| Requirement links | FR-05, FR-06 |
| Preconditions | UC-06 or UC-07 has supplied a profile and a published opportunity with a reviewed rule set. |
| Main success flow | Evaluate each applicable mandatory rule as pass, fail or unresolved; apply failure-first decision precedence; include UC-15 Generate Eligibility Explanation; return the structured result. |
| Alternative / exception flow | Missing inputs, incompatible scales and unsupported mandatory conditions remain unresolved. An execution failure must not return a fabricated eligible result. |
| Postconditions | A consistent status, criterion outcomes and explanation are returned to the calling use case. |

### UC-15 — Generate Eligibility Explanation

| Field | Description |
| --- | --- |
| Actor / invocation | Included system behavior; no independent actor |
| Requirement links | FR-08 |
| Preconditions | Criterion outcomes and relevant recorded requirements are available. |
| Main success flow | Build an understandable explanation of passed, failed and unresolved conditions, identifying the requirement and relevant applicant information; return it with source-verification context. |
| Alternative / exception flow | Do not invent reasons or represent unknown information as a confirmed pass/failure. |
| Postconditions | The calling evaluation receives a traceable explanation. |

## 6. Outstanding Detailed Decisions

Scoring weights and tie handling, presentation of potentially eligible recommendations, supported qualification/test vocabularies, deadline cutoff interpretation, and maximum comparison count remain subject to the decisions listed in the FR/NFR document. These are not represented as completed implementation choices.

## 7. Next Deliverable

Prepare a Class Diagram and justified design-pattern selection from these responsibilities. Model domain classes and services, rather than turning every use case into a class.
