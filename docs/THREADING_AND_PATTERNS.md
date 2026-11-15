# ScholarshipMatch: design patterns and threading

## Implemented patterns

1. **Strategy (behavioral):** `EligibilityStrategy` defines `evaluate(profile, scholarship)`. Degree, field and CGPA strategies implement separate rules.
2. **Simple Factory (creational):** `EligibilityRuleFactory.create(rule_key)` returns the correct strategy. Unsupported keys raise `ValueError`.
3. **Facade (structural):** `ScholarshipMatchFacade.recommend(profile, records)` provides one entry point to evaluate and sort results.

The Singleton scoring-configuration idea in the original proposal is not implemented in this phase. Do not present it as completed.

## Threading implementation

`ScholarshipMatchFacade` uses Python's `concurrent.futures.ThreadPoolExecutor` with a maximum of four worker threads. Each task assesses one scholarship against the same read-only profile snapshot. `executor.map` preserves the input result order before the facade applies its own recommendation sort.

The Flask route retrieves the profile and active scholarship records before starting the pool. The workers receive ordinary Python data only. They do not access Flask request globals, session data, or a shared PyMySQL connection. This boundary is important because the database connection is request-scoped and must not be shared between worker threads.

## Current rule scope and limitations

The existing database schema currently stores target degree, field, minimum CGPA, country, funding type and deadline. Only degree, field and minimum CGPA are treated as mandatory eligibility criteria. Country and funding are shown as preferences. The match score is 25% degree + 25% field + 50% CGPA. A past deadline changes the result status to Closed and prevents it from being marked eligible. This is a preliminary matching aid, not a guarantee of a scholarship award.

## Verification

`tests/test_recommendations.py` covers factory selection, unsupported rule rejection, each strategy, successful and failed matches, all-fields acceptance, expired deadlines, empty input and execution on named worker threads. Run:

```powershell
.\.venv\Scripts\Activate.ps1
pytest -q
```

The test environment should use `requirements-dev.txt`. The real MySQL integration test is opt-in and must target a separate database ending in `_test`.
