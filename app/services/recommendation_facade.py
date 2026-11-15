"""Recommendation facade and safe concurrent evaluation orchestration."""
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime

from .eligibility_strategies import EligibilityRuleFactory


class ScholarshipMatchFacade:
    """Provide one entry point for assessing a profile against scholarships."""

    RULES = ("degree", "field", "cgpa")
    MAX_WORKERS = 4

    def recommend(self, profile, scholarship_records):
        if not profile:
            return []
        records = list(scholarship_records or [])
        if not records:
            return []

        # Each worker receives ordinary Python data only. MySQL access is done
        # by the caller before this point; request-scoped connections are never
        # shared between worker threads.
        workers = min(self.MAX_WORKERS, len(records))
        with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="sm-eligibility") as pool:
            results = list(pool.map(self._assess_one, ((profile, item) for item in records)))

        results.sort(key=self._sort_key)
        return results

    def _assess_one(self, pair):
        profile, scholarship = pair
        checks = [EligibilityRuleFactory.create(rule).evaluate(profile, scholarship)
                  for rule in self.RULES]
        score = sum(check["weight"] for check in checks if check["passed"])

        deadline = scholarship.get("deadline")
        if isinstance(deadline, datetime):
            deadline = deadline.date()
        elif isinstance(deadline, str) and deadline:
            try:
                deadline = date.fromisoformat(deadline)
            except ValueError:
                deadline = None

        is_closed = bool(deadline and deadline < date.today())
        eligible = all(check["passed"] for check in checks)
        status = "Closed" if is_closed else ("Eligible" if eligible else "Not eligible")
        preferences = {
            "country_matches": profile.get("preferred_country") in ("any", scholarship.get("country")),
            "funding_matches": profile.get("preferred_funding") in ("any", scholarship.get("funding")),
        }
        return {
            "scholarship": scholarship,
            "checks": checks,
            "score": score,
            "eligible": eligible and not is_closed,
            "status": status,
            "is_closed": is_closed,
            "preferences": preferences,
        }

    @staticmethod
    def _sort_key(result):
        deadline = result["scholarship"].get("deadline")
        if isinstance(deadline, datetime):
            deadline = deadline.date()
        if not isinstance(deadline, date):
            deadline = date.max
        return (not result["eligible"], -result["score"], deadline,
                result["scholarship"].get("title", "").casefold())
