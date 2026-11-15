"""Unit tests for eligibility strategies, factory, facade and thread execution."""
from datetime import date, timedelta
from decimal import Decimal

import pytest

from app.services.eligibility_strategies import (
    CGPAStrategy, DegreeStrategy, EligibilityRuleFactory, FieldStrategy,
)
from app.services.recommendation_facade import ScholarshipMatchFacade


@pytest.fixture
def profile():
    return {
        "degree": "undergraduate",
        "field": "Software Engineering",
        "cgpa": Decimal("3.50"),
        "preferred_country": "Germany",
        "preferred_funding": "fully_funded",
    }


@pytest.fixture
def scholarship():
    return {
        "id": 1,
        "title": "Engineering Scholarship",
        "provider": "Example Foundation",
        "country": "Germany",
        "degree": "undergraduate",
        "field": "Software Engineering",
        "funding": "fully_funded",
        "min_cgpa": Decimal("3.00"),
        "deadline": date.today() + timedelta(days=30),
    }


def test_factory_returns_correct_strategy_types():
    assert isinstance(EligibilityRuleFactory.create("degree"), DegreeStrategy)
    assert isinstance(EligibilityRuleFactory.create("field"), FieldStrategy)
    assert isinstance(EligibilityRuleFactory.create("cgpa"), CGPAStrategy)


def test_factory_rejects_unknown_rule():
    with pytest.raises(ValueError, match="Unsupported eligibility rule"):
        EligibilityRuleFactory.create("nationality")


def test_strategy_results_are_correct(profile, scholarship):
    assert DegreeStrategy().evaluate(profile, scholarship)["passed"] is True
    assert FieldStrategy().evaluate(profile, scholarship)["passed"] is True
    assert CGPAStrategy().evaluate(profile, scholarship)["passed"] is True
    scholarship["min_cgpa"] = Decimal("3.80")
    assert CGPAStrategy().evaluate(profile, scholarship)["passed"] is False


def test_facade_returns_eligible_match_with_weighted_score(profile, scholarship):
    result = ScholarshipMatchFacade().recommend(profile, [scholarship])[0]
    assert result["status"] == "Eligible"
    assert result["eligible"] is True
    assert result["score"] == 100
    assert all(check["passed"] for check in result["checks"])


def test_facade_identifies_failed_criteria(profile, scholarship):
    scholarship["field"] = "Medicine"
    scholarship["min_cgpa"] = Decimal("3.80")
    result = ScholarshipMatchFacade().recommend(profile, [scholarship])[0]
    assert result["status"] == "Not eligible"
    assert result["score"] == 25
    assert [c["key"] for c in result["checks"] if not c["passed"]] == ["field", "cgpa"]


def test_all_fields_is_accepted(profile, scholarship):
    scholarship["field"] = "All fields"
    assert FieldStrategy().evaluate(profile, scholarship)["passed"] is True


def test_expired_scholarship_is_closed(profile, scholarship):
    scholarship["deadline"] = date.today() - timedelta(days=1)
    result = ScholarshipMatchFacade().recommend(profile, [scholarship])[0]
    assert result["status"] == "Closed"
    assert result["eligible"] is False


def test_facade_handles_missing_profile_and_empty_catalogue(scholarship):
    facade = ScholarshipMatchFacade()
    assert facade.recommend(None, [scholarship]) == []
    assert facade.recommend({}, []) == []


def test_facade_runs_evaluations_in_worker_threads(profile, scholarship, monkeypatch):
    thread_names = []
    facade = ScholarshipMatchFacade()
    original = facade._assess_one

    def capture(pair):
        import threading
        thread_names.append(threading.current_thread().name)
        return original(pair)

    monkeypatch.setattr(ScholarshipMatchFacade, "_assess_one", staticmethod(capture))
    records = [dict(scholarship, id=index, title=f"Scholarship {index}") for index in range(8)]
    results = facade.recommend(profile, records)
    assert len(results) == 8
    assert thread_names
    assert all(name.startswith("sm-eligibility") for name in thread_names)


def test_recommendation_page_requires_login(client):
    response = client.get("/recommendations")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_recommendation_page_prompts_for_profile(client):
    from .helpers import register, login
    register(client)
    login(client)
    response = client.get("/recommendations")
    assert response.status_code == 200
    assert b"Complete your academic profile first" in response.data


def test_recommendation_page_renders_database_results(client, monkeypatch):
    from app.repository import profiles, scholarships
    from .helpers import register, login
    register(client)
    login(client)
    monkeypatch.setattr(profiles, "find", lambda user_id: {
        "degree": "undergraduate", "field": "Software Engineering",
        "cgpa": Decimal("3.50"), "preferred_country": "Germany",
        "preferred_funding": "fully_funded",
    })
    monkeypatch.setattr(scholarships, "list_all", lambda: [{
        "id": 5, "title": "Engineering Scholarship", "provider": "Example Foundation",
        "country": "Germany", "degree": "undergraduate",
        "field": "Software Engineering", "funding": "fully_funded",
        "min_cgpa": Decimal("3.00"), "deadline": date.today() + timedelta(days=30),
    }])
    response = client.get("/recommendations")
    assert response.status_code == 200
    assert b"Engineering Scholarship" in response.data
    assert b"100" in response.data
    assert b"Eligible" in response.data
