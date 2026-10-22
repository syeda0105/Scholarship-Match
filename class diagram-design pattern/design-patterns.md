# ScholarshipMatch — Design Pattern Selection

**Student:** Syeda Alysha Aly  
**Registration:** F24-BSSE-110  
**Course:** Software Construction & Development  
**Date:** 20 October 2026  
**Status:** Proposed design for implementation

## 1. Overview

ScholarshipMatch will use MVC, Factory, Facade and Singleton for distinct design responsibilities. Patterns are selected for a problem, not assigned one per module. MVC organizes the web application; Factory handles eligibility evaluator creation; Facade coordinates assessment and recommendation operations; Singleton supplies a consistent scoring configuration within an application process.

The attached teaching documents demonstrate these concepts in Java. This project applies the concepts in Python/Flask. Flask does not automatically enforce this architecture; the project must organize its components deliberately.

## 2. MVC — Model–View–Controller

**Problem:** Mixing HTML, request handling, database operations and eligibility logic makes changes and testing difficult.

**Application:** Domain models such as User, ApplicantProfile and Scholarship represent application data. Jinja HTML templates and CSS form the view. Flask route handlers/controllers validate requests, enforce access rules and delegate work to services before rendering results. Decision services and repositories support the model/business responsibilities without placing calculations in templates.

**Example:** An applicant requests an eligibility check. ScholarshipController delegates to the facade and renders the returned result in an eligibility template.

**Benefit:** Presentation changes do not require rewriting rule evaluation. The decision engine can be tested without a browser.

**Classification:** Application architectural/presentation pattern; it is not one of the GoF creational, structural or behavioral patterns.

## 3. Factory — Eligibility Evaluator Creation

**Problem:** Each stored eligibility criterion needs the appropriate evaluator. Repeated construction conditionals across controllers would duplicate knowledge of rule types.

**Application:** EligibilityRuleFactory.create(definition) returns an evaluator implementing the EligibilityRule contract, such as AcademicResultRule, NationalityRule or QualificationRule. Other supported evaluator types can use the same contract. Unknown or unsupported mandatory conditions are handled as unresolved, never silently ignored.

**Example:** A stored academic-threshold definition requests AcademicResultRule; a nationality definition requests NationalityRule. EligibilityEngine invokes evaluate through the common interface.

**Benefit:** Evaluator selection is centralized, and adding a supported rule type does not require changing every caller.

**Classification:** Creational. Precisely, this is a **Simple Factory**, matching the shape-factory approach in the supplied document; it is not the GoF Factory Method based on overriding creator subclasses.

## 4. Facade — Assessment and Recommendation Entry Point

**Problem:** Controllers should not manually coordinate data loading, mandatory rule checking, scoring and explanation assembly on every request.

**Application:** ScholarshipMatchFacade exposes assess(profile_id, scholarship_id) and recommend(profile_id). It delegates to repositories, EligibilityEngine, MatchScorer and ExplanationGenerator. It does not implement every rule internally or replace backend authentication/authorization.

**Example:** The recommendations controller makes one facade call. The facade loads candidate data, obtains assessments, excludes ineligible/closed opportunities, scores suitable candidates and returns explained results.

**Benefit:** Simpler controllers and one consistent orchestration path across related features.

**Classification:** Structural.

## 5. Singleton — Shared Scoring Configuration

**Problem:** Recommendation components within one running application process should use the same validated scoring-weight snapshot rather than accidentally using different copies or hard-coded values.

**Application:** ScoringConfiguration provides one instance through get_instance(). It is initialized during application startup and exposes immutable weights and a configuration version. MatchScorer reads from it. Construction must be controlled; merely calling an ordinary class a singleton is insufficient.

**Example:** Every scorer in the process reads the same configured weights. No applicant profile, session or active database connection is stored on this object.

**Benefit:** Centralized and consistent configuration in the process.

**Limits and implementation discipline:** A Python singleton is process-local, not one object shared across all hosting workers. All workers must load the same configuration version. Initial loading should occur before concurrent requests; live weight editing is outside the initial implementation. Configuration changes can take effect through a controlled restart/reload. Tests must be able to inject configuration rather than depending on hidden global state. A normal injected configuration object would also be a valid engineering alternative; the explicit singleton here is a deliberate academic design choice, not an inherent requirement of Flask.

**Classification:** Creational.

## 6. Summary

| Pattern | Participants | Responsibility |
| --- | --- | --- |
| MVC | Models, Jinja templates, Flask controllers | Separate data/business responsibilities, presentation and request handling |
| Simple Factory | EligibilityRuleFactory, EligibilityRule and concrete rule evaluators | Create the appropriate evaluator from a stored rule type |
| Facade | ScholarshipMatchFacade and assessment/scoring collaborators | Coordinate a complete result through a simple entry point |
| Singleton | ScoringConfiguration | Provide one immutable scoring configuration instance per application process |

## 7. Validation Plan

- Verify that controllers delegate decision logic and templates display results without recalculating eligibility.
- Verify that the factory returns the correct evaluator and unsupported mandatory rules remain unresolved.
- Verify facade behavior for passing, failed, incomplete and expired-opportunity scenarios.
- Verify repeated singleton access returns the same object in one process and weights cannot be mutated by a request.
- Verify mandatory failures cannot be overridden by preferences and profile data never leaks through shared configuration.

These checks are planned, not yet executed. See [class design](class-diagram.md), [use cases](use-cases.md) and [requirements](functional-and-non-functional-requirements.md) for context.
