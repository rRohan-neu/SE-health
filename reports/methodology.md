# Methodology | Employer fit and pilot scenario

## Research question
Which employer types appear promising for an initial SE Bridge pilot, considering caregiver reach, eligibility, learning potential, provider coverage and absence context?

## Evidence hierarchy
1. Employer administrative information (headcount, eligibility).
2. Provider-verified service coverage.
3. Official Statistics Canada industry context.
4. Explicit assumptions where no observed data exists.

Every variable should record source, period, geography, unit and status (`observed`, `derived`, `proxy`, `assumption`).

## Caregiver proxy
Statistics Canada's 2018 GSS analysis provides caregiver prevalence by age group. Combining age-mix shares with these rates can create a broad proxy. It is not an industry-specific caregiver rate and is historical.

## Fit score
Default weights: caregiver reach 30%, eligibility 20%, pilot learning potential 20%, provider reachability 15%, absence pressure 15%. The weights are judgment-based, not trained on pilot outcomes. Pilot learning reaches full marks at 12 expected users; this is a design threshold requiring SE Health review.

## Absence pressure
Table 14-10-0191-01 reports days lost per full-time employee by industry. The score maps 0 days to 0 and 8+ days to 100. This is a display normalization, not a causal estimate of preventable absence.

## Simulation and validation
Monte Carlo distributions represent uncertainty around assumed inputs. They are not empirical distributions until calibrated. Recruit contrasting pilots (healthcare, rural employer with verified coverage, frontline retail), freeze predictions before launch, measure the employee funnel and service utilization, compare actual results with predicted ranges, and revise assumptions. Use a defensible comparison design before attributing absence changes to SE Bridge.
