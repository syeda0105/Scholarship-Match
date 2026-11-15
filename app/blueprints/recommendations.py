"""Authenticated scholarship eligibility and recommendation page."""
from flask import Blueprint, g, render_template

from app.blueprints.auth import login_required
from app.repository import profiles, scholarships
from app.services.recommendation_facade import ScholarshipMatchFacade

bp = Blueprint("recommendations", __name__)
_facade = ScholarshipMatchFacade()


@bp.get("/recommendations")
@login_required
def index():
    profile = profiles.find(g.user["id"])
    items = scholarships.list_all()
    results = _facade.recommend(profile, items) if profile else []
    return render_template("recommendations.html", profile=profile, results=results)
