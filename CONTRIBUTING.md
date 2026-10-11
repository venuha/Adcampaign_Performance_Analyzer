# Contributing

## Set up

Use Python 3.12 and a virtual environment. Install `requirements-dev.txt` and
run `streamlit run app.py` from the repository root.

## Make changes

- Put CSV validation in `campaign_analyzer/data.py`.
- Keep metric calculations in `metrics.py` and define their units explicitly.
- Keep shared filters and period aggregation in `filters.py`.
- Build figures in `charts.py` and Streamlit controls in `dashboard.py` or `ui/`.
- Add regression tests for changed calculations, validation, and interactions.
- Update the README or data dictionary when behavior changes.

Avoid averaging percentages across records. Recompute rates from their
summed numerators and denominators. Preserve unavailable values when a
denominator is zero.

## Before opening a pull request

```bash
python -m ruff format .
python -m ruff check .
python -m unittest discover -s tests -v
```

Include the concrete problem, resulting behavior, and validation performed.
Use fictional data in tests and examples. Keep private datasets and credentials
outside tracked files.
