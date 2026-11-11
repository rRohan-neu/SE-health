# Data source register

| Source | Identifier / date | Variables | Interpretation |
|---|---|---|---|
| Statistics Canada, labour force by industry and age | Table 14-10-0023-01 | Labour force characteristics by NAICS, gender and age group | Use employment measure for workforce age mix; distinguish labour force from employment and inspect suppressed cells |
| Statistics Canada, work absence by industry | Table 14-10-0191-01 | Annual days lost per full-time employee by NAICS and sex | Industry context; not preventable absence |
| Statistics Canada, work absence by age | Table 14-10-0193-01 | Annual days lost per full-time employee by age group and sex | Age context; separate table, not age-by-industry |
| Statistics Canada, older caregivers article | General Social Survey 2018 | Caregiver prevalence by age | Population proxy, not industry-specific |
| Employer questionnaire | Pilot-specific | Headcount, eligibility, shift profile, age mix | Employer-reported; validate definitions |
| SE Health operations | Pilot-specific | Service geography and provider reach | Provider-verified; date-stamp coverage |

Statistics Canada caregiver prevalence values used in `src/caregiving.py` are 2018 GSS age-band estimates: 15–24 (21.6%), 25–34 (16.8%), 35–44 (20.4%), 45–54 (32.9%), 55–64 (33.9%), 65–74 (26.9%), 75–84 (22.4%), and 85+ (13.3%). Source: https://www150.statcan.gc.ca/n1/pub/75-006-x/2020001/article/00007-eng.htm
