# ScholarshipMatch — Requirements Baseline

| Document field | Value |
| --- | --- |
| Project | ScholarshipMatch: Intelligent Scholarship Eligibility & Recommendation System |
| Author | Syeda Alysha Aly |
| Registration number | F24-BSSE-110 |
| Programme | BS Software Engineering |
| Course | Software Construction & Development |
| Stage | 2 — Requirements Baseline |
| Version | 0.1 |
| Date | 20 October 2026 |
| Status | Working draft — scope and business rules documented; FR/NFR refinement pending |

## 1. Document Purpose

This document records the project scope, user responsibilities, data-maintenance approach and proposed business rules developed after the project proposal. It provides a foundation for functional and non-functional requirements, use cases, class design and testing.

This version is not a completed Software Requirements Specification (SRS). Business rules are proposed for review, and unresolved decisions are listed explicitly. Implementation and testing have not yet been completed.

## 2. Project Overview

ScholarshipMatch is a web-based decision-support system that compares applicant profiles with structured scholarship eligibility criteria. It provides explained eligibility assessments and weighted recommendations, helping applicants identify suitable opportunities and prepare for application requirements and deadlines.

The system evaluates recorded criteria. It does not guarantee admission or scholarship selection, and applicants submit applications through the official provider's channel.

## 3. Objectives

- Reduce the manual effort required to compare applicant profiles with scholarship requirements.
- Distinguish mandatory eligibility criteria from applicant preferences.
- Explain satisfied criteria, failed criteria and information requiring verification.
- Rank suitable opportunities using a transparent scoring method.
- Support scholarship comparison, saved opportunities, requirement checklists and deadline tracking.
- Allow administrators to maintain verified scholarship records and rules.

## 4. Stakeholders and Roles

| Stakeholder or role | Responsibility or interest |
| --- | --- |
| Student / Applicant | Maintains a profile and uses eligibility checks, recommendations and preparation features. |
| Administrator | Maintains scholarship records, eligibility rules, source references and verification information. |
| Scholarship provider | Publishes official criteria and receives applications through its own channel; no provider account is planned in ScholarshipMatch. |
| Project developer | Designs, implements, tests and documents the semester project. |
| Course evaluator | Reviews the project's requirements, design, implementation and demonstration. |

Administrator and Student/Applicant are the two planned application roles. The other stakeholders are not additional login roles.

### 4.1 Role Boundaries

| Function | Student / Applicant | Administrator |
| --- | --- | --- |
| Register a standard applicant account | Yes | Administrator access is provisioned separately |
| Maintain an academic and preference profile | Yes | Not required for administrative work |
| Browse and filter scholarship opportunities | Yes | Available as needed for review |
| Check eligibility and view recommendations | Yes | Not required for administrative work |
| Compare and save opportunities | Yes | Not required for administrative work |
| Maintain personal requirement checklists | Yes | No access to another applicant's checklist by default |
| Add, edit, activate or archive scholarships | No | Yes |
| Maintain eligibility rules and verification information | No | Yes |

The Add Scholarship form belongs to the protected administrator interface. Standard registration must not allow an applicant to grant themselves administrator privileges. Administrative authorization must be enforced by the backend, not only by hiding interface controls.

## 5. Scope

### 5.1 Included in the Planned Semester Version

- User registration, authentication and role-based access.
- Applicant academic profiles and scholarship preferences.
- Administrator-maintained scholarship records and structured eligibility criteria.
- Scholarship browsing and filtering.
- Rule-based eligibility evaluation with explanations.
- Weighted recommendation scoring and ranking.
- Comparison of selected scholarships.
- Saved scholarships and personal requirement checklists.
- Display of upcoming deadlines for saved opportunities.
- Official source links, application-cycle information and verification dates.

These are planned capabilities, not claims of completed functionality.

### 5.2 Outside the Initial Scope

- Automatic scholarship scraping or external data imports.
- Machine-learning model training.
- Submission of scholarship applications to providers.
- Storage of uploaded passports, transcripts or other application documents.
- Paid APIs, paid AI integrations and purchased domains.
- Guaranteed scholarship selection or exhaustive evaluation of every provider condition.

Document readiness will be represented through checklist status rather than document uploads. Automated email or SMS reminders are not required for the initial version; deadline display remains in scope.

## 6. Scholarship Data and System Operation

An administrator reviews official sources and enters scholarship details through an administrative form. The backend validates the request and saves the scholarship and its structured criteria in MySQL. Applicant-facing pages and decision services use those stored records.

| Item | Intended handling |
| --- | --- |
| Initial data collection | Manual review of official scholarship sources |
| Data entry and corrections | Protected administrator forms; routine updates do not require code changes |
| Source evidence | Official source URL, application cycle and last verification date |
| Eligibility processing | Automatic evaluation of the stored mandatory rules against applicant information |
| Recommendations | Automatic scoring and ranking under defined eligibility and scoring rules |
| Deadline handling | Exclude expired opportunities from open recommendations |
| Deadline extensions or new cycles | Administrator verification and record update |

Saving a source link does not automatically synchronize its contents. Scholarship criteria must be represented as structured data for the eligibility engine to evaluate them. Automatic expiry detection does not discover provider deadline extensions.

## 7. Business Rules

| ID | Business rule |
| --- | --- |
| BR-01 | Only administrators may create, modify, activate or archive scholarship records and their eligibility rules. |
| BR-02 | Each published scholarship opportunity must include an official source URL, application cycle, deadline with timezone, and last verification date. |
| BR-03 | Eligibility shall be assessed against the mandatory criteria recorded for the selected scholarship opportunity. |
| BR-04 | If any evaluated mandatory criterion is not satisfied, the eligibility result shall be **Ineligible**, even when other required information is missing. |
| BR-05 | If no mandatory criterion has failed but information needed to evaluate a mandatory criterion is missing or unresolved, the result shall be **Potentially Eligible — Verification Required**. |
| BR-06 | The result shall be **Eligible Against Recorded Criteria** only when all recorded mandatory criteria have been evaluated and satisfied. |
| BR-07 | Preference scores shall not override mandatory eligibility failures. Ineligible opportunities shall be excluded from personalized recommendations but may remain available for browsing with explanations. |
| BR-08 | Expired or archived opportunities shall be excluded from open recommendations. A new application cycle must be verified before an opportunity is reopened. |
| BR-09 | Academic results shall be compared using compatible grading scales. The system shall not invent conversions or eligibility thresholds. |
| BR-10 | Eligibility assessment does not guarantee admission or scholarship selection. Applications shall be submitted through the official provider's application channel. |

### 7.1 Eligibility Decision Precedence

| Priority | Condition | Result |
| --- | --- | --- |
| 1 | At least one mandatory criterion has failed | Ineligible |
| 2 | No mandatory criterion has failed, but at least one required assessment is missing or unresolved | Potentially Eligible — Verification Required |
| 3 | All recorded mandatory criteria have been evaluated and satisfied | Eligible Against Recorded Criteria |

“Potentially Eligible” indicates an incomplete assessment, not a probability of selection. Missing or unresolved criteria must be identified in the explanation.

### 7.2 Opportunity Status Versus Applicant Eligibility

An opportunity's application status and an applicant's eligibility are separate concepts. An academically eligible applicant may be viewing a closed opportunity. Expiry must not be described as an academic eligibility failure, and closed opportunities must not appear in open recommendations.

### 7.3 Illustrative Rule Scenarios

The following examples describe intended behavior and are not executed test results.

| Scenario | Expected behavior | Related rules |
| --- | --- | --- |
| Required CGPA is 3.00/4.00; applicant CGPA is 2.80/4.00; funding and country preferences match | Return Ineligible; explain the CGPA failure regardless of preference matches. | BR-04, BR-07 |
| No checked rule fails, but a required test result is unknown | Return Potentially Eligible — Verification Required and identify the missing result. | BR-05 |
| A nationality rule fails and a required test result is unknown | Return Ineligible, explaining the failure and identifying the unresolved check. | BR-04 |
| All recorded mandatory criteria pass | Return Eligible Against Recorded Criteria with criterion-level explanations. | BR-06, BR-10 |
| An opportunity's deadline has passed | Exclude it from open recommendations without treating expiry as an academic failure. | BR-08 |
| Applicant and scholarship grades use incompatible scales without an approved conversion | Flag the grade check as unresolved; do not invent a conversion. Apply overall decision precedence. | BR-05, BR-09 |

## 8. Constraints and Proposed Technical Direction

- The project is an individual semester project with a zero-payment budget.
- Development must use tools and dependencies available without mandatory payment.
- Public deployment is an intended deliverable; hosting choices must be checked against current free-plan limits before use.
- The proposed stack remains Java with Spring Boot, MySQL, HTML, CSS, JavaScript and Bootstrap.
- Git and GitHub will track source code and project documentation.
- Database credentials, secret keys and real applicant personal data must not be committed to the repository.
- Scholarship entry is administrator-maintained in the initial version; automated data importing is a future enhancement.

## 9. Pending Decisions and Remaining Stage 2 Work

| ID | Pending item | Required outcome |
| --- | --- | --- |
| PD-01 | Supported study levels | Confirm master's only or undergraduate, master's and PhD support; no narrowing has yet been approved. |
| PD-02 | Profile fields and supported rule types | Define required inputs, supported tests, grading scales and treatment of unsupported conditions. |
| PD-03 | Recommendation calculation | Finalize scoring criteria, weights, normalization and treatment of potentially eligible opportunities. Proposal weights remain illustrative. |
| PD-04 | Functional requirements | Refine the proposal's preliminary FR-01 through FR-11 into clear, testable requirements without losing agreed features. |
| PD-05 | Non-functional requirements | Refine usability, performance, security, reliability, maintainability and traceability requirements with practical acceptance conditions. |
| PD-06 | Data-maintenance procedure | Define validation before publication, handling of uncertain criteria and a feasible review schedule. |

## 10. Stage Completion and Next Deliverables

Stage 2 will be complete when scope and business rules are reviewed, the study-level decision is resolved, and functional/non-functional requirements have clear acceptance conditions. This version documents the work completed so far and does not claim that milestone has been reached.

Subsequent deliverables:

1. Use Case Diagram and main use case descriptions.
2. Class Diagram and justified design-pattern selection.
3. Database ERD, data dictionary and interface wireframes.
4. Incremental implementation and requirement-linked testing.

## 11. Document Basis and Change History

This draft is based on `ScholarshipMatch_Syeda_Alysha_Aly_Proposal.docx` and the subsequent project discussions on scope, roles, data maintenance and business rules. The original proposal remains the source for preliminary functional and non-functional requirements; they are not yet finalized by this document.

| Version | Date | Change |
| --- | --- | --- |
| 0.1 | 20 October 2026 | Recorded scope, roles, data approach, BR-01–BR-10, decision examples and pending Stage 2 work. |
