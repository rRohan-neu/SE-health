import pytest
from src.simulation import PilotAssumptions, simulate_pilot, summarize_simulation

def test_simulation_reproducible():
    a = PilotAssumptions(500, .27, .75)
    assert simulate_pilot(a, 200, 7).equals(simulate_pilot(a, 200, 7))

def test_invalid_share_rejected():
    with pytest.raises(ValueError):
        simulate_pilot(PilotAssumptions(100, 1.2, .5), 10)

def test_summary_percentiles_ordered():
    df = simulate_pilot(PilotAssumptions(100, .25, .8), 100)
    s = summarize_simulation(df)
    assert s["users"]["low"] <= s["users"]["median"] <= s["users"]["high"]
