# SE Bridge | Workforce Intelligence

A reproducible research and decision-support prototype for assessing where an employer-sponsored caregiver-support service may be useful.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.pipeline --download
python -m src.pipeline --build
streamlit run dashboard/app.py
pytest
```
The dashboard works without downloaded data using scenario inputs. Demo inputs are illustrative, not observations.

## Data sources
- [Statistics Canada 14-10-0023-01](https://doi.org/10.25318/1410002301-eng): annual labour force characteristics by industry, gender and age group (employment and unemployment; inspect the measure before using).
- [Statistics Canada 14-10-0191-01](https://doi.org/10.25318/1410019101-eng): annual work absence of full-time employees by industry.
- [Statistics Canada 14-10-0193-01](https://doi.org/10.25318/1410019301-eng): annual work absence by age group.
- [Statistics Canada 2018 GSS caregiving analysis](https://www150.statcan.gc.ca/n1/pub/75-006-x/2020001/article/00007-eng.htm): caregiver prevalence by age; population-level proxy, not industry-specific.

The pipeline downloads Statistics Canada's full-table CSV ZIPs for industry-by-age labour force context and work absence by industry/age, retains raw files, records SHA-256 hashes and retrieval metadata, and creates analysis extracts. Inspect table dimensions and labels before selecting categories.

## Model
The employer fit score (0–100) uses five transparent components: caregiver reach (30%), benefit eligibility (20%), pilot learning potential (20%), provider reachability (15%) and absence pressure (15%). Weights and normalization thresholds are judgment-based design choices, not fitted coefficients.

The Monte Carlo pilot scenario estimates users, service hours, cost and illustrative absence value from explicit assumptions. It is not a causal estimate, a validated forecast, or proof that SE Bridge prevents absences.

## Research integrity
- National industry averages are not employer-specific estimates.
- Age-based caregiver prevalence is a proxy, not an industry-specific rate.
- Industry absence days are context, not preventable absences.
- Eligibility and provider coverage require employer/provider verification.
- Uptake, utilization, costs and outcomes require pilot measurement.
- Do not claim validation until prospective predictions are compared with observed pilot outcomes.

See `reports/methodology.md`, `reports/data_sources.md`, `survey/` and `gis/README.md`. The `src/caregiving.py` module calculates an age-mix-weighted population proxy; `src/analysis.py` provides reusable table summaries and rank-sensitivity analysis.
