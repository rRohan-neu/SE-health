from dataclasses import dataclass

DEFAULT_WEIGHTS = {
    "caregiver_reach": 0.30, "eligibility": 0.20, "pilot_learning": 0.20,
    "provider_reachability": 0.15, "absence_pressure": 0.15,
}

@dataclass
class EmployerProfile:
    industry: str
    headcount: int
    caregiver_share: float
    eligibility_share: float
    provider_reachability: float
    annual_absence_days: float
    likely_uptake: float = 0.20
    shift_work_share: float = 0.0
    rural_share: float = 0.0

def _bounded(x):
    return max(0.0, min(100.0, float(x)))

def score_employer(profile: EmployerProfile, weights: dict | None = None) -> dict:
    w = weights or DEFAULT_WEIGHTS
    if set(w) != set(DEFAULT_WEIGHTS) or abs(sum(w.values()) - 1.0) > 1e-8:
        raise ValueError("Provide all five weights and ensure they sum to 1.0")
    if profile.headcount < 0:
        raise ValueError("headcount cannot be negative")
    for name in ("caregiver_share", "eligibility_share", "provider_reachability", "likely_uptake"):
        if not 0 <= getattr(profile, name) <= 1:
            raise ValueError(f"{name} must be between 0 and 1")
    expected_users = profile.headcount * profile.caregiver_share * profile.eligibility_share * profile.likely_uptake
    components = {
        "caregiver_reach": _bounded(profile.caregiver_share * 100),
        "eligibility": _bounded(profile.eligibility_share * 100),
        "pilot_learning": _bounded(expected_users / 12 * 100),
        "provider_reachability": _bounded(profile.provider_reachability * 100),
        # Transparent display scale: 8+ annual days lost maps to 100; not a benchmark.
        "absence_pressure": _bounded(profile.annual_absence_days / 8 * 100),
    }
    total = sum(components[k] * w[k] for k in w)
    weakest = min(components, key=components.get)
    tier = "Strong fit" if total >= 70 else "Good fit" if total >= 55 else "Possible" if total >= 40 else "Low fit"
    return {"fit_score": round(total, 1), "tier": tier,
            "components": {k: round(v, 1) for k, v in components.items()},
            "weights": w, "main_limit": weakest,
            "expected_users_90d": round(expected_users, 1)}
