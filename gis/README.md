# GIS / provider coverage analysis

Use organization worksite locations and provider-approved service areas to determine practical reach. Rurality alone does not establish service availability.

Workflow:
1. Obtain current provider-approved service communities or polygons.
2. Obtain employer worksite addresses/coordinates only (never employee homes).
3. Geocode using an approved service and document match quality.
4. Join worksites to provider service polygons or calculate travel-time bands.
5. Aggregate by municipality / FSA / region and calculate covered workforce share.
6. Validate gaps with SE Health operations.

Tools: GeoPandas, QGIS, Folium and Statistics Canada boundary files. Suppress small counts and do not map identifiable employees, patients or care recipients.

Suggested schema: `worksite_id, organization_id, municipality, province, latitude, longitude, employee_count, provider_coverage_status, coverage_reference_date`.
