import pytest
from src.caregiving import AGE_CAREGIVER_RATES_2018, estimate_caregiver_share

def test_equal_age_mix_returns_average_rate():
    mix = {k: 1 / len(AGE_CAREGIVER_RATES_2018) for k in AGE_CAREGIVER_RATES_2018}
    estimate = estimate_caregiver_share(mix)
    assert 0.1 < estimate < 0.4

def test_age_mix_must_sum_to_one():
    mix = {k: 0.1 for k in AGE_CAREGIVER_RATES_2018}
    with pytest.raises(ValueError):
        estimate_caregiver_share(mix)
