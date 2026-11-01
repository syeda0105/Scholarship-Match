# ScholarshipMatch — Database Design (Logical ERD)

| Field | Value |
| --- | --- |
| Student | Syeda Alysha Aly |
| Registration | F24-BSSE-110 |
| Course | Software Construction & Development |
| Stage | 5A — Database Design |
| Version / Date | 0.1 / 20 October 2026 |
| Status | Initial logical design; SQL schema and database integration are not yet implemented |

## 1. Purpose

This design translates the requirements and class responsibilities into persistent relational data for MySQL. The ERD is split into two views of the same database. The users table appears in both views as a reference; it is created only once.

Inputs: [requirements](functional-and-non-functional-requirements.md), [use cases](use-cases.md) and [class design](class-diagram.md).

## 2. ERD Views

### Accounts and Profiles

![Account and profile ERD](diagrams/erd-accounts.png)

### Scholarships and Application Preparation

![Scholarship and preparation ERD](diagrams/erd-scholarships.png)

[Editable two-page Draw.io ERD](diagrams/scholarshipmatch-erd.drawio)

The PNG views use explicit minimum/maximum cardinalities. The editable source uses crow's-foot notation. Each line joins the parent table to the child table whose foreign key refers to it. Selected columns are shown, not a complete SQL schema.

## 3. Table Responsibilities

| Table | Stored information | Main constraint |
| --- | --- | --- |
| users | Account email, password hash, role and creation time | Unique email; public registration creates applicants only |
| applicant_profiles | Personal eligibility context, intended degree and field | At most one profile per account; administrative accounts need no applicant profile |
| qualifications | Current/completed education, field, result and grading scale | Each qualification belongs to one profile; qualification level is separate from target degree |
| test_results | Test type, known/unknown result status, score and date | Each record belongs to one profile; unknown must not be stored as a passing score |
| profile_country_preferences | Applicant-preferred destination country codes | Composite primary key (profile_id, country_code) prevents duplicates |
| profile_funding_preferences | Applicant-preferred funding categories | Composite primary key (profile_id, funding_type) prevents duplicates |
| scholarships | One opportunity/application cycle, publication metadata, source and deadline | Activation requires reviewed criteria and complete source/deadline metadata |
| eligibility_rules | Structured mandatory conditions and unresolved provider requirements | Each definition belongs to one scholarship and has validated type-specific parameters |
| scholarship_documents | Named preparation requirements for an opportunity | One scholarship may list several document requirements |
| saved_scholarships | The relationship between an applicant account and a saved opportunity | Unique (user_id, scholarship_id) |
| checklist_items | Applicant-reported readiness for a document on a saved opportunity | Unique (saved_scholarship_id, scholarship_document_id); both references must concern the same scholarship |

There are eleven logical tables. The two preference tables avoid comma-separated lists and support multiple preferences. They are not separate modules or dashboards.

## 4. Relationship Rules

1. One user has zero or one applicant profile. Every profile belongs to exactly one user.
2. One profile has zero or more qualifications, tests, country preferences and funding preferences. Each child belongs to exactly one profile.
3. One scholarship has zero or more rules and document requirements while in draft. Activation requires an adequate reviewed rule set; an empty or unsupported rule set cannot silently produce an eligible result.
4. Users and scholarships have a many-to-many saved relationship, resolved by saved_scholarships. Every saved record has exactly one user and one scholarship.
5. A saved opportunity has zero or more readiness records. A scholarship document may be referenced by zero or more applicants' readiness records.
6. The scholarship_id in checklist_items is a consistency field. The physical schema will use composite foreign keys against (saved_scholarship_id, scholarship_id) and (scholarship_document_id, scholarship_id), supported by unique parent indexes. This prevents linking a saved opportunity to a document belonging to another scholarship. It is not an independent choice the applicant can change.
7. The additional checklist_items.scholarship_id reference is not drawn as a separate line to avoid clutter. Profile and scholarship identifiers in the diagrams are keys, not role authorization by themselves.

## 5. Preparation Checklist Behavior

The displayed checklist is based on active scholarship_documents for the saved opportunity. A checklist_items record is created or updated when the applicant reports readiness. An absent readiness record is displayed as not ready, so saving an opportunity does not require pre-creating every checklist row.

Readiness remains applicant-reported; it does not prove that a provider has approved a document. It does not override academic eligibility. If a new document requirement is added, it appears as not ready unless the applicant marks it otherwise. Requirements that are retired are marked inactive rather than deleting rows still referenced by readiness records.

Document preparation requirements and mandatory eligibility rules are distinct. If a document is itself a mandatory eligibility condition, it must also have an explicit supported rule or an unresolved mandatory condition; a checked preparation box is not automatically verification.

## 6. Structured Eligibility Rules

eligibility_rules stores data, while Python evaluator classes implement behavior. Each row has a rule_type and validated JSON parameters. This is a controlled representation of varying rules, not executable Python or SQL supplied by administrators.

Examples, for illustration only:

| Rule type | Example parameters | Interpretation |
| --- | --- | --- |
| ACADEMIC_RESULT | {"minimum": 3.0, "scale": "CGPA_4"} | Compare only against a supported compatible result |
| NATIONALITY | {"allowed_codes": ["PK"]} | Applicant nationality must be allowed |
| QUALIFICATION | {"required_level": "BACHELORS", "in_progress_allowed": false} | Require the stated prior qualification/completion policy |
| AGE | {"maximum": 30, "reference_date": "2027-01-01", "inclusive": true} | Check age on the specified date under a documented interpretation |
| UNSUPPORTED | {"requirement_text": "Provider-specific condition requiring review"} | Produce an unresolved mandatory result if marked mandatory |

Exact rule vocabulary and schemas must be finalized with the data dictionary. Database JSON validity alone is insufficient: backend validation must check the supported rule type, required keys, ranges and interpretation. Unstated thresholds and grading conversions must not be invented.

## 7. Stored Versus Calculated Data

| Persist in this version | Calculate when requested |
| --- | --- |
| Accounts and profiles | Eligibility status and individual rule outcomes |
| Qualifications and tests | Match score and ranking |
| Scholarship records and source metadata | Plain-language eligibility explanation |
| Eligibility rule definitions | Open/closed status from publication state and deadline |
| Saved associations and readiness | Upcoming deadline order and comparison display |

EligibilityResult, RuleOutcome and Recommendation from the class design are initially response/value objects, not history tables. Re-evaluating after profile or rule changes uses current data. Historical assessment snapshots can be a later enhancement.

The initial immutable scoring configuration is maintained in application configuration with a version, not a new database table. This is consistent with the proposed ScoringConfiguration component.

## 8. Data Integrity and Security Decisions

- Passwords are stored only as salted hashes generated by a maintained hashing facility.
- Database credentials and application secrets remain outside committed files.
- Ownership and administrator checks are enforced by the backend on every protected action. Foreign keys cannot replace these checks.
- Result values retain their grading scale. A missing result is not zero, and incompatible scales remain unresolved unless an approved conversion is explicitly supported.
- Prior qualification vocabulary must include higher secondary and other supported qualifications, not only the three target study levels.
- Store the deadline instant in UTC together with the original IANA timezone for interpretation/display. Date-only or ambiguous source deadlines require explicit verification before a precise cutoff is published.
- New annual cycles are separate opportunity records. Do not overwrite a closed cycle and silently reinterpret existing saved records as a new application.
- Archive scholarship records instead of routine hard deletion. Block hard deletion of referenced parent records in the initial schema. Any future account deletion procedure must be deliberately designed.
- Use transactions for multi-table operations and parameterized queries for database access.
- Country codes, funding categories, test types and qualification levels use validated vocabularies, to be specified in Stage 5B. No lookup tables are required in this initial design, but they may be introduced if requirements justify them.

## 9. Traceability

| Requirements | Main tables |
| --- | --- |
| FR-01 | users |
| FR-02 | applicant_profiles, qualifications, test_results, profile_country_preferences, profile_funding_preferences |
| FR-03 | scholarships |
| FR-04–FR-08 | scholarships and eligibility_rules, together with profile data; calculated results are not persisted |
| FR-09 | scholarships and eligibility_rules |
| FR-10 | saved_scholarships, scholarship_documents, checklist_items |
| FR-11 | saved_scholarships and scholarships |

## 10. Next Step — Data Dictionary

Stage 5B will define exact column names, MySQL types, nullability, defaults, indexes, foreign keys, allowed values and validation rules. It will also finalize rule parameter schemas and deadline interpretation policies needed before affected features are accepted. The logical tables above may be refined if a constraint requires it.

After the data dictionary, create initial UI wireframes and a runnable schema. Then implement and verify the registration/login slice with the local MySQL service. This document does not claim that WampServer is installed or the application is connected to a database.
