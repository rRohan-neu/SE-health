# Power BI / Excel data dictionary

Pipeline extracts retain source dimensions rather than silently aggregating them. Typical fields include:
- `REF_DATE`: reference period
- `GEO`: geography
- `DGUID`: geography identifier
- table-specific dimensions (industry, age group, sex, absence measure)
- `VALUE`: numeric estimate
- `STATUS`: estimate status / symbol metadata

Inspect actual column names and labels after download. Recommended star-schema tables: `DimIndustry`, `DimYear`, `FactAbsenceIndustry`, `FactAbsenceAge`, `EmployerProfile`, `PilotOutcomes`.

Recommended visuals: annual industry absence trend; industry comparison by selected measure; separate age-group absence comparison; employer fit component breakdown; pilot funnel; forecast-vs-actual results.
