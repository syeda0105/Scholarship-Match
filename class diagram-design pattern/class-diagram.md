# ScholarshipMatch — Class Design

| Field | Value |
| --- | --- |
| Author / Registration | Syeda Alysha Aly / F24-BSSE-110 |
| Date / Version | 20 October 2026 / 0.1 |
| Status | Initial design, not implemented class inventory |

## 1. Scope

The class design is split into domain and application views to keep it readable. Together they describe the same application. Python annotations are conceptual; exact persistence mappings, signatures and validation will be refined during implementation. This is not an ERD and does not require every displayed class to become a database table.

Inputs: [requirements](functional-and-non-functional-requirements.md), [use cases](use-cases.md), and [business rules](requirements-baseline.md).

## 2. Domain View

![Domain Class Diagram](diagrams/class-diagram.png)

## 3. Application and Pattern View

![Application and Patterns Class Diagram](diagrams/design-patterns-class-diagram.png)

[Editable two-page Draw.io source](diagrams/class-diagram.drawio)

Multiplicity labels read from the first class to the second. For example, User–SavedScholarship “1 to 0..*” means one user has zero or more saved associations; SavedScholarship–Scholarship “0..* to 1” means each saved association refers to exactly one scholarship. Composition diamonds mark the owner. Dashed references on calculated results do not require persisted historical records.

## 4. Class Responsibilities and Constraints

| Class | Responsibility / constraint |
| --- | --- |
| User | Account identity, password hash and stored role. A user has zero or one applicant profile; an administrator need not have one. Email is unique. |
| ApplicantProfile | Qualification context, intended study level, nationality, birth date and preferences. Evaluation results reference exactly one profile even where that reference is not drawn separately. |
| QualificationRecord | Current or completed qualification and its result/scale. Multiple qualifications are permitted; target degree is a different concept. |
| TestResult | Applicant test information and explicitly known/unknown results. |
| Scholarship | One opportunity/application cycle with publication metadata and deadline. Degree/field/nationality conditions are configured in its rule definitions. Funding/country may contribute to preferences. |
| EligibilityRuleDefinition | Stored rule type and parameters. This is data, not executable behavior. A reviewed opportunity must have an adequate rule set; zero stored rules must not accidentally imply eligibility. |
| SavedScholarship | Applicant-specific association with an opportunity. The user/scholarship pair is unique. |
| ChecklistItem | Applicant-reported readiness attached to a saved opportunity. Templates may be derived from recorded scholarship document requirements; checklist creation details will be refined with the ERD. |
| EligibilityResult | A calculated status, time, explanation and outcomes for one profile/opportunity. Not necessarily stored. Closed/open status remains independent. |
| RuleOutcome | Pass, fail or unresolved result for a recorded mandatory rule, with expected/actual values and reason. |
| Recommendation | Calculated score and breakdown for a scholarship with its associated assessment. This is not automatically a database table. |
| ScholarshipController | Flask request handling, input/ownership checks, delegation and rendering or response creation. It does not own the decision algorithm. |
| ScholarshipMatchFacade | Coordinates repositories, engine, scorer and explanation generator through simple assessment and recommendation methods. |
| ScholarshipRepository | Reads/writes scholarship data using parameterized queries and managed connections. Actual MySQL connections are not singleton objects. |
| EligibilityEngine | Evaluates mandatory rules and applies failure-first precedence. Receives time explicitly for reproducible deadline/age checks. |
| EligibilityRuleFactory | Constructs an evaluator implementing EligibilityRule from a supported stored rule type. Unsupported conditions produce unresolved outcomes through explicit handling. |
| EligibilityRule | Common evaluate contract, represented in Python by an abstract base class or a documented protocol. |
| AcademicResultRule | Compares compatible grading scales and thresholds; does not invent conversions. |
| NationalityRule | Evaluates allowed nationalities against profile data. |
| QualificationRule | Evaluates required prior qualification, target degree and supported completion policies. |
| MatchScorer | Calculates transparent match scores using shared configuration, after eligibility gating. |
| ExplanationGenerator | Converts rule outcomes and source context into clear reasons; no paid AI service is required. |
| ScoringConfiguration | One immutable application-process configuration snapshot for scoring weights and version. |

Additional supported age, field and test evaluators will implement the same interface; three representative implementations are shown to keep the diagram readable. ProfileRepository and UserRepository provide profile/account persistence but are omitted from the focused pattern view. Authentication will use an AuthController/AuthService pair for registration, password verification, sessions and logout; User holds account data rather than handling HTTP sessions. These components must be detailed when implementing FR-01. HTML templates and static CSS are the MVC view, not Python domain classes.

## 5. Enumerations and Value Types

| Type | Intended values / interpretation |
| --- | --- |
| UserRole | APPLICANT, ADMIN |
| DegreeLevel | UNDERGRADUATE, MASTERS, PHD; prior-qualification vocabulary also includes higher secondary and must be finalized |
| QualificationStatus | IN_PROGRESS, COMPLETED |
| EligibilityStatus | ELIGIBLE_RECORDED_CRITERIA, POTENTIALLY_ELIGIBLE_VERIFICATION_REQUIRED, INELIGIBLE |
| RuleStatus | PASS, FAIL, UNRESOLVED |
| PublicationStatus | DRAFT, ACTIVE, ARCHIVED; open/closed is derived using publication status and deadline |
| Rule parameters | Validated structured values for thresholds, scale, allowed values, reference dates or an explicitly unsupported condition |

Birth date and reference dates support age checks; a single unqualified “age” number is insufficient. Deadlines must be timezone-aware. Supported grading scales and conversions, exact scoring and maximum comparison count remain open as recorded in the requirements.

## 6. Traceability

| Requirements | Main design elements |
| --- | --- |
| FR-01 | User; planned AuthController/AuthService and UserRepository |
| FR-02 | ApplicantProfile, QualificationRecord, TestResult; planned ProfileRepository |
| FR-03–FR-04 | Scholarship, EligibilityRuleDefinition, ScholarshipRepository; administrative controllers |
| FR-05–FR-06 | EligibilityEngine, EligibilityRuleFactory, EligibilityRule, EligibilityResult, RuleOutcome |
| FR-07–FR-08 | ScholarshipMatchFacade, MatchScorer, ScoringConfiguration, Recommendation, ExplanationGenerator |
| FR-09 | ScholarshipController and scholarship query/comparison operations |
| FR-10–FR-11 | SavedScholarship, ChecklistItem, Scholarship deadline; applicant-specific persistence and controllers |

## 7. Review Notes

This initial model communicates the central domain and selected patterns. It does not claim to exhaust every controller, repository or association. Before coding each feature, refine its classes and database mapping against its acceptance checks. Authorization, CSRF protection, transactions and password hashing are implementation requirements even when not expressed as individual domain classes. The class model and ERD must be kept consistent as decisions are finalized.
