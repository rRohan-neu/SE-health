from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import streamlit as st
import plotly.express as px
from src.fit_score import EmployerProfile, score_employer
from src.simulation import PilotAssumptions, simulate_pilot, summarize_simulation

st.set_page_config(page_title="SE Bridge | Workforce Intelligence", page_icon="📊", layout="wide")
st.title("SE Bridge | Workforce Intelligence")
st.caption("Canadian labour-market context • Employer fit assessment • Pilot scenario modelling")
st.warning("Prototype only. Inputs are illustrative assumptions unless explicitly employer/provider verified.")

with st.sidebar:
    st.header("Employer profile")
    industry = st.selectbox("Industry", ["Hospital / health employer", "Rural manufacturer",
        "Office / professional services", "Community home care", "Retail / frontline services",
        "Community non-profit", "Other"])
    headcount = st.number_input("Employees", 1, 100000, 500, 25)
    caregiver = st.slider("Estimated caregiver share", 0.0, 1.0, .27, .01)
    eligibility = st.slider("Benefits-eligible share", 0.0, 1.0, .75, .01)
    reach = st.slider("Provider-verified service coverage", 0.0, 1.0, .80, .01)
    absence = st.number_input("Annual absence days / FTE", 0.0, 30.0, 7.0, .1)
    uptake = st.slider("Expected uptake among eligible caregivers", 0.0, 1.0, .20, .01)
    st.divider()
    st.subheader("Pilot economics")
    hours_month = st.number_input("Hours / user / month", 0.0, 100.0, 4.0, .5)
    cost_hour = st.number_input("Service cost / hour ($)", 0.0, 500.0, 35.0, 1.0)
    addressable = st.number_input("Potentially addressable absence days / user / year", 0.0, 30.0, .5, .1)
    value_day = st.number_input("Value per avoided absence day ($)", 0.0, 5000.0, 250.0, 25.0)
    months = st.selectbox("Pilot duration (months)", [1, 3, 6, 12], index=1)

profile = EmployerProfile(industry, int(headcount), caregiver, eligibility, reach, absence, uptake)
fit = score_employer(profile)
scenario = simulate_pilot(PilotAssumptions(int(headcount), caregiver, eligibility, uptake,
    hours_month, cost_hour, addressable, value_day, reach, months))
summary = summarize_simulation(scenario)

a, b, c = st.columns(3)
a.metric("Fit score", f"{fit['fit_score']}/100", fit["tier"])
b.metric("Expected users (90-day score input)", f"{fit['expected_users_90d']:.1f}")
c.metric("Main constraint", fit["main_limit"].replace("_", " ").title())

st.subheader("Fit score components")
comp = pd.DataFrame({"Component": [k.replace("_", " ").title() for k in fit["components"]],
                     "Score": list(fit["components"].values()),
                     "Weight (%)": [v * 100 for v in fit["weights"].values()]})
st.plotly_chart(px.bar(comp, x="Component", y="Score", range_y=[0, 100], hover_data=["Weight (%)"]),
                use_container_width=True)
st.dataframe(comp, hide_index=True, use_container_width=True)

st.subheader("Pilot scenario range (P10 / median / P90)")
cols = st.columns(4)
for col, key, label, prefix in [(cols[0], "users", "Users", ""),
    (cols[1], "service_hours", "Service hours", ""),
    (cols[2], "service_cost", "Service cost", "$"),
    (cols[3], "absence_value_scenario", "Illustrative absence value", "$")]:
    v = summary[key]
    col.metric(label, f"{prefix}{v['median']:,.1f}",
               f"P10–P90: {v['low']:,.1f}–{v['high']:,.1f}")
st.caption("P10–P90 is a scenario interval, not a statistical confidence interval or guaranteed outcome.")
st.plotly_chart(px.histogram(scenario, x="net_value_scenario", nbins=40,
    labels={"net_value_scenario": "Scenario net value ($)"}), use_container_width=True)
st.download_button("Download fit components CSV", comp.to_csv(index=False),
    "se_bridge_fit_components.csv", "text/csv")
st.download_button("Download simulation CSV", scenario.to_csv(index=False),
    "se_bridge_pilot_simulation.csv", "text/csv")

st.subheader("Official data pipeline")
processed = Path(__file__).resolve().parents[1] / "data" / "processed"
for f in ["labour_force_industry_age.csv", "absence_industry.csv", "absence_age.csv"]:
    st.write(("✓ " if (processed / f).exists() else "○ ") + f)
st.info("The official Statistics Canada extracts are retained as tidy source-dimension data. Before charting, select the correct measure, sex, geography and reference year from table labels.")
