from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class PilotAssumptions:
    headcount: int
    caregiver_share: float
    eligibility_share: float
    uptake_mean: float = 0.20
    monthly_hours_per_user: float = 4.0
    service_cost_per_hour: float = 35.0
    addressable_absence_days_per_user_year: float = 0.5
    value_per_absence_day: float = 250.0
    provider_reachability: float = 0.80
    months: int = 3

def simulate_pilot(a: PilotAssumptions, n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Scenario simulation; distributions are assumptions until calibrated with pilot data."""
    if a.headcount < 0 or a.months <= 0 or n <= 0:
        raise ValueError("headcount must be nonnegative; months and n must be positive")
    for field in ("caregiver_share", "eligibility_share", "uptake_mean", "provider_reachability"):
        if not 0 <= getattr(a, field) <= 1:
            raise ValueError(f"{field} must be between 0 and 1")
    rng = np.random.default_rng(seed)
    def beta_draw(mean, concentration):
        if mean <= 0: return np.zeros(n)
        if mean >= 1: return np.ones(n)
        return rng.beta(mean * concentration, (1 - mean) * concentration, n)
    caregivers = beta_draw(a.caregiver_share, 70)
    eligible = beta_draw(a.eligibility_share, 60)
    uptake = beta_draw(a.uptake_mean, 25)
    reach = beta_draw(a.provider_reachability, 35)
    users = a.headcount * caregivers * eligible * uptake * reach
    hours = users * a.monthly_hours_per_user * a.months
    cost = hours * a.service_cost_per_hour
    potential_days = users * a.addressable_absence_days_per_user_year * a.months / 12
    avoided_days = potential_days * rng.beta(2, 8, n)  # assumed realization share, mean 20%
    value = avoided_days * a.value_per_absence_day
    return pd.DataFrame({"users": users, "service_hours": hours, "service_cost": cost,
        "absence_days_avoided_scenario": avoided_days, "absence_value_scenario": value,
        "net_value_scenario": value - cost})

def summarize_simulation(df: pd.DataFrame) -> dict:
    cols = ["users", "service_hours", "service_cost", "absence_days_avoided_scenario",
            "absence_value_scenario", "net_value_scenario"]
    return {c: {label: float(df[c].quantile(p)) for label, p in
            [("low", .10), ("median", .50), ("high", .90)]} for c in cols}
