"""Population age-specific caregiver rates used only as an explicitly labelled proxy."""
AGE_CAREGIVER_RATES_2018 = {
    "15-24": 0.216, "25-34": 0.168, "35-44": 0.204, "45-54": 0.329,
    "55-64": 0.339, "65-74": 0.269, "75-84": 0.224, "85+": 0.133,
}

def estimate_caregiver_share(age_mix: dict[str, float]) -> float:
    """Weighted population proxy from an employer/industry age mix.

    `age_mix` must contain the eight age bands as proportions summing to 1.
    These 2018 population rates are not industry-specific and should not be
    interpreted as measured caregiver prevalence for a particular employer.
    """
    if set(age_mix) != set(AGE_CAREGIVER_RATES_2018):
        raise ValueError("age_mix must contain all eight documented age bands")
    if any(v < 0 or v > 1 for v in age_mix.values()):
        raise ValueError("age shares must be between 0 and 1")
    if abs(sum(age_mix.values()) - 1.0) > 1e-6:
        raise ValueError("age shares must sum to 1.0")
    return sum(age_mix[age] * rate for age, rate in AGE_CAREGIVER_RATES_2018.items())
