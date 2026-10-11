# Architecture

`app.py` calls `campaign_analyzer.dashboard.main()` and contains no analysis
logic. The package runs from the repository root without an editable install.

## Data flow

1. `data.load_data()` reads the uploaded CSV or bundled synthetic CSV.
2. `data.validate_data()` checks the schema, values, grain, and metadata.
3. `dashboard.main()` builds the shared sidebar and calls `filters.filter_data()`.
4. Every view receives the same filtered DataFrame.
5. `metrics.aggregate()` sums additive measures and calculates weighted rates.
6. `charts.py` creates figures; `ui/components.py` renders charts and tables.

The analysis functions do not depend on Streamlit, making them independently
testable. Streamlit-specific code stays in `dashboard.py` and `ui/`.
Sample paths derive from `config.PROJECT_ROOT`, rather than the caller's
working directory or a personal filesystem path.

## Test boundaries

- Data tests cover validation failures and text identifier preservation.
- Metric tests check totals, weighted ratios, zero denominators, and empty groups.
- Filter tests check inclusive dates, combined selections, literal search, and
  Monday week boundaries.
- App tests exercise all four views, shared filters, search, and empty states.

The prototype does not connect to ad platform APIs, infer attribution, adjust
for product costs, or provide persistent storage. Revenue-based comparisons
must use comparable campaign objectives.
