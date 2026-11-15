"""Eligibility rules implemented with the Strategy and Simple Factory patterns.

Only criteria represented by the current database schema are evaluated here:
qualification level, field of study, and minimum CGPA. Country and funding
preferences are shown as preferences, not misrepresented as mandatory rules.
"""
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation


class EligibilityStrategy(ABC):
    """Common interface for one independently evaluated eligibility rule."""

    key = ""
    weight = 0

    @abstractmethod
    def evaluate(self, profile, scholarship):
        """Return a consistent rule result dictionary."""


class DegreeStrategy(EligibilityStrategy):
    key = "degree"
    weight = 25

    def evaluate(self, profile, scholarship):
        passed = profile.get("degree") == scholarship.get("degree")
        return {"key": self.key, "label": "Target degree", "passed": passed, "weight": self.weight,
                "detail": "Degree level matches" if passed else "Degree level does not match"}


class FieldStrategy(EligibilityStrategy):
    key = "field"
    weight = 25

    def evaluate(self, profile, scholarship):
        required = scholarship.get("field")
        passed = required == "All fields" or profile.get("field") == required
        return {"key": self.key, "label": "Field of study", "passed": passed, "weight": self.weight,
                "detail": "Your field is accepted" if passed else f"Required field: {required}"}


class CGPAStrategy(EligibilityStrategy):
    key = "cgpa"
    weight = 50

    def evaluate(self, profile, scholarship):
        try:
            actual = Decimal(str(profile.get("cgpa")))
            minimum = Decimal(str(scholarship.get("min_cgpa")))
            passed = actual >= minimum
        except (InvalidOperation, TypeError, ValueError):
            passed = False
            minimum = scholarship.get("min_cgpa", "not specified")
        return {"key": self.key, "label": "Minimum CGPA", "passed": passed, "weight": self.weight,
                "detail": "CGPA requirement met" if passed else f"Minimum required: {minimum}"}


class EligibilityRuleFactory:
    """Create the concrete evaluator for a supported rule identifier."""

    _strategies = {
        "degree": DegreeStrategy,
        "field": FieldStrategy,
        "cgpa": CGPAStrategy,
    }

    @classmethod
    def create(cls, rule_key):
        strategy_class = cls._strategies.get(rule_key)
        if strategy_class is None:
            raise ValueError(f"Unsupported eligibility rule: {rule_key}")
        return strategy_class()
