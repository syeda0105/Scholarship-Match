# ScholarshipMatch — Functional and Non-Functional Requirements

| Field | Value |
| --- | --- |
| Author | Syeda Alysha Aly |
| Registration number | F24-BSSE-110 |
| Course | Software Construction & Development |
| Stage | 2 — Requirements Baseline |
| Version | 0.2 |
| Date | 20 October 2026 |
| Status | Requirements draft for design; acceptance checks are planned, not executed |

## 1. Purpose and Relationship to Earlier Documents

This document refines the proposal's eleven functional requirements and quality requirements into a basis for use cases, class design and testing. Read it with [Requirements Baseline](requirements-baseline.md), which contains scope, roles and BR-01–BR-10.

Where the earlier baseline lists study levels or backend technology as pending or proposed, the decisions below take precedence. The earlier baseline's pending items are not evidence that these two decisions remain open. This document does not claim that the application has been implemented or tested.

## 2. Recorded Scope and Technology Decisions

- Support undergraduate, master's and PhD scholarship opportunities in a limited, verified catalogue.
- Use one application and shared eligibility engine, with scholarship-specific criteria.
- Record current/completed qualifications separately from the intended degree level; evaluate final-year applicants according to the scholarship's stated policy.
- Use Python with Flask for the backend, HTML/CSS/JavaScript with Bootstrap for the frontend, and MySQL for persistent data. Python/Flask replaces the Java/Spring Boot proposal.
- Use VS Code for development. WampServer may provide the local MySQL service; it does not require a PHP backend.
- Maintain scholarship data through a protected administrator interface using verified official sources. External imports and scraping remain outside initial scope.
- Provide document-readiness checklists without storing uploaded application documents.
- Keep mandatory eligibility decisions separate from preference scores.
- Use free development tools and avoid mandatory paid APIs or subscriptions. Hosting feasibility must be verified before deployment.

## 3. Roles and Access

| Role | Main responsibilities |
| --- | --- |
| Applicant | Maintain a personal profile, discover opportunities, request assessments, view recommendations, compare and save scholarships, and track readiness and deadlines. |
| Administrator | Maintain scholarship records, eligibility criteria, official source links and verification information. |

Public registration creates applicant accounts only. Administrator access is provisioned separately. Applicants must not access another applicant's private profile, saved items or checklist.

## 4. Functional Requirements and Acceptance Checks

The FR-01–FR-11 identifiers from the proposal are retained. Each row may require several test cases. Acceptance checks describe expected behavior, not completed validation.

| ID | Functional requirement | Planned acceptance checks |
| --- | --- | --- |
| FR-01 | The system shall allow applicants to register, log in and log out. Public registration shall create applicant accounts only. | Valid registration creates one applicant account. Duplicate email registration is rejected. Correct credentials establish a session; incorrect credentials do not. Logout invalidates the session. Protected actions require authentication. Public input cannot assign administrator privileges. |
| FR-02 | The system shall allow applicants to create and update their academic profiles and scholarship preferences. | Save and reload current/completed qualification information, intended degree, field, nationality, date of birth, grading value and scale, relevant test status/scores, and country/funding preferences. Reject invalid values; allow explicitly unknown optional information without converting it into a passing check. Another applicant cannot edit the profile. |
| FR-03 | The system shall allow authorized administrators to add, edit, activate and archive scholarship opportunities, including official source URLs, application cycles, deadlines with timezone and verification dates. | A valid administrative submission persists after reload. Publishing requires the metadata in BR-02 and a reviewed rule set. Edits appear in subsequent views and assessments. Archived records do not appear in open recommendations. Applicant requests to administrative operations are rejected by the backend. |
| FR-04 | The system shall allow authorized administrators to maintain structured eligibility rules for each scholarship opportunity. | Store applicable qualification, target degree, academic threshold/scale, field, nationality, age and test rules. Validate rule configuration. Distinguish an explicitly unrestricted criterion from an unknown requirement. Record unsupported mandatory conditions as requiring verification. Do not invent unstated thresholds. |
| FR-05 | The system shall evaluate an applicant's profile against the recorded mandatory criteria of a selected scholarship opportunity. | Evaluate applicable rules using current saved inputs. Collect pass, fail or unresolved outcomes. Exercise undergraduate, master's and PhD examples. Assess incompatible grading scales or unsupported conditions as unresolved unless an approved interpretation is available. |
| FR-06 | The system shall classify an assessment as Eligible Against Recorded Criteria, Potentially Eligible — Verification Required, or Ineligible according to the business rules. | Any mandatory failure yields Ineligible, including when another check is unresolved. With no failures, an unresolved mandatory check yields Potentially Eligible — Verification Required. Only a fully evaluated passing rule set yields Eligible Against Recorded Criteria. A draft/unreviewed opportunity cannot yield an eligible result. |
| FR-07 | The system shall calculate match scores using defined criteria and weights and display ranked recommendations without allowing preference scores to override mandatory eligibility failures. | Published scoring weights and calculation rules reproduce displayed scores within the defined rounding tolerance. Ineligible, expired and archived opportunities are excluded from open recommendations. Potentially eligible opportunities are clearly identified. Exact weights, tie handling and presentation grouping must be finalized before implementation acceptance. |
| FR-08 | The system shall display satisfied criteria, failed criteria and missing or unresolved information for each eligibility assessment. | Display a reason for every evaluated rule, indicating the relevant requirement and applicant information where appropriate. Unknown information is not shown as a confirmed failure or pass. Show the official source, verification date and a statement that eligibility does not guarantee selection. |
| FR-09 | The system shall allow applicants to browse and filter scholarship opportunities and compare selected opportunities side by side. | Filters for target degree, country, funding type and field produce records satisfying the selected filters. A no-result state is clear. Compare two selected opportunities on consistent fields, including deadlines, funding and eligibility requirements. Confirm the maximum comparison count during UI design. |
| FR-10 | The system shall allow applicants to save and unsave scholarship opportunities and update their personal requirement-checklist status. | A saved item persists after login again. Saving the same opportunity does not create duplicates. Unsaving removes the saved association. Checklist changes persist and are private to their owner. Checklist completion alone does not change mandatory academic eligibility. |
| FR-11 | The system shall display upcoming deadlines for saved opportunities and indicate when a saved opportunity has closed. | Upcoming deadlines are shown in chronological order with clear timezone information. Before/at/after-deadline boundary cases follow the documented cutoff rule. Closed saved items remain identifiable as closed and are excluded from open recommendations. No automatic next-cycle reopening occurs. |

## 5. Non-Functional Requirements and Acceptance Checks

The following are proposed semester-project targets. Performance figures are acceptance targets, not measured results. A recorded test environment and representative dataset are required for meaningful evaluation.

| ID | Quality attribute | Requirement and planned verification |
| --- | --- | --- |
| NFR-01 | Usability | Registration, profile validation and eligibility results shall use plain-language labels and field-specific errors. Verify that required fields, missing information and the three assessment statuses are distinguishable without relying on colour alone. |
| NFR-02 | Responsive interface | Core applicant and administrator screens shall remain usable at viewport widths of 360 px, 768 px and 1366 px. Verify that forms and primary controls have no unintended page-level horizontal overflow; comparison tables may use a clearly contained horizontal scroll area. |
| NFR-03 | Performance | In a documented local test environment, using 100 scholarship opportunities with up to 10 recorded mandatory rules each, at least 19 of 20 repeated search or recommendation requests shall complete within 2 seconds after warm-up. Measure server request-processing time and record hardware, data and test method. Free-host startup delays are measured separately, not hidden as normal evaluation time. |
| NFR-04 | Authentication and authorization | Passwords shall be stored as salted hashes using a maintained password-hashing facility, never plaintext. Verify backend role checks, protection against cross-account access, parameterized database queries, CSRF protection on state-changing browser forms, and rejection of invalid sessions. Use HTTPS and appropriately protected session cookies for public deployment. |
| NFR-05 | Privacy and configuration | Collect only profile information required by supported functions. Do not store uploaded application documents. Database credentials and application secrets shall be supplied through local/environment configuration and excluded from version control. Verify that repository contents and user-facing errors do not expose credentials or password hashes. |
| NFR-06 | Reliability and correctness | The same profile, rule set, scoring configuration and evaluation time shall produce the same substantive result. Verify failure precedence, unknown information, equality thresholds, deadline boundaries and grading-scale mismatches. Failed saves shall not leave partially committed related records. |
| NFR-07 | Maintainability | Scholarship criteria and scoring configuration shall be maintainable without editing presentation templates. Separate request handling, data access and decision logic into identifiable components. Verify that changing a stored threshold affects a subsequent assessment without changing the rule evaluator's source code. New rule types may require code changes. |
| NFR-08 | Traceability and transparency | Each displayed assessment shall identify its scholarship/application cycle, evaluation time, criterion-level outcomes and source verification information. Maintain a requirements-to-use-case-and-test mapping in project documentation. Historical assessment storage is not required by this version. |
| NFR-09 | Data integrity and error handling | Validate profile values, rule configurations and deadline inputs on the server. Enforce unique account emails and valid record relationships. Database failures shall produce a controlled message rather than a stack trace or success message. Verify that invalid writes do not corrupt existing data. |
| NFR-10 | Reproducible setup and deployment | Maintain dependency records, schema/setup scripts, a configuration example without secrets and README instructions. Verify setup from a clean environment and test the intended public deployment before submission. Keep a local demonstration path and documented database backup/restore procedure because free hosting may be unavailable or suspended. |

## 6. Eligibility and Opportunity Status

| Situation | Required interpretation |
| --- | --- |
| At least one mandatory check fails | Ineligible, regardless of preferences or other unresolved checks |
| No mandatory failure; at least one mandatory check is unresolved | Potentially Eligible — Verification Required |
| Reviewed rule set; every recorded mandatory check passes | Eligible Against Recorded Criteria |
| Application deadline has passed | Opportunity is closed; this is separate from academic eligibility |
| A document checklist item is marked ready | Applicant-reported readiness; not provider verification or a guaranteed eligibility pass |

All three degree levels use these same decision rules. The catalogue does not claim to cover all scholarships or to automatically assess every possible provider condition.

## 7. Business-Rule Traceability

| Business rules in the baseline | Related functional requirements | Related quality requirements |
| --- | --- | --- |
| BR-01: Administrator-only maintenance | FR-01, FR-03, FR-04 | NFR-04, NFR-05 |
| BR-02: Source and cycle metadata | FR-03, FR-08 | NFR-08, NFR-09 |
| BR-03–BR-06: Eligibility assessment and precedence | FR-04, FR-05, FR-06, FR-08 | NFR-01, NFR-06, NFR-08 |
| BR-07: Preferences cannot override failures | FR-07 | NFR-06, NFR-08 |
| BR-08: Expired/archived opportunities | FR-03, FR-07, FR-11 | NFR-06, NFR-09 |
| BR-09: Compatible grading scales | FR-02, FR-04, FR-05, FR-08 | NFR-06, NFR-09 |
| BR-10: Official application channel and no selection guarantee | FR-03, FR-08 | NFR-01, NFR-08 |

## 8. Remaining Detailed Decisions

These items are explicitly open. They do not prevent an initial use case model, but must be resolved before the affected implementation is accepted.

1. Exact scoring formula, weights, treatment of incomplete profiles, ranking groups and tie handling. Proposal weights are illustrative.
2. Supported qualification vocabulary, test types, grading scales and any source-approved conversion policy.
3. Exact age reference-date handling, final-year qualification policies, multiple-deadline handling and deadline cutoff interpretation.
4. Publication review checklist and practical re-verification schedule for scholarship data.
5. Comparison limit, precise profile-field validation and supported browser test versions.

Until a condition has a supported interpretation, it must remain explicitly unresolved rather than being silently ignored.

## 9. Next Design Deliverables

1. Use Case Diagram with Applicant and Administrator actors.
2. Main use case descriptions linked to FR identifiers.
3. Class Diagram and justified design patterns adapted to Python/Flask.
4. ERD, data dictionary and interface wireframes.

Implementation may proceed in small increments alongside refinement. Completion of a document is not evidence of completed code or passed tests.

## 10. Change Record

| Version | Date | Changes |
| --- | --- | --- |
| 0.2 | 20 October 2026 | Recorded support for all three degree levels, Python/Flask technology change, refined FR-01–FR-11, proposed NFR targets, acceptance checks and business-rule traceability. |
