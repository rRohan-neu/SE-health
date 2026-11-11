import pytest
from src.fit_score import EmployerProfile, score_employer

def profile(**kwargs):
    d = dict(industry="Test", headcount=500, caregiver_share=.27,
             eligibility_share=.75, provider_reachability=.8, annual_absence_days=7)
    d.update(kwargs)
    return EmployerProfile(**d)

def test_score_is_bounded_and_explainable():
    r = score_employer(profile())
    assert 0 <= r["fit_score"] <= 100
    assert len(r["components"]) == 5
    assert r["tier"] in {"Strong fit", "Good fit", "Possible", "Low fit"}

def test_zero_headcount_has_no_expected_users():
    r = score_employer(profile(headcount=0))
    assert r["expected_users_90d"] == 0

def test_invalid_share_rejected():
    with pytest.raises(ValueError):
        score_employer(profile(caregiver_share=1.2))
