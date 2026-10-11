# Online deployment

The app runs as a Python server. GitHub stores the source code; a hosting
service runs it and provides the browser URL.

## Streamlit Community Cloud

Deploy the existing GitHub project without changing its framework:

1. Sign in at https://share.streamlit.io/.
2. Select **Create app** and deploy an app from GitHub.
3. Set repository to `venuha/Adcampaign_Performance_Analyzer`.
4. Set branch to `main` and main file path to `app.py`.
5. In **Advanced settings**, select Python **3.12**.
6. Choose an available app URL and deploy.
7. Confirm the overview loads, then test a filter, Reset Filters, the campaign
   funnel, and a CSV upload on the public app.

`requirements.txt` supplies the runtime dependencies. No API key is required.
The included synthetic sample is suitable for a public demo. Uploaded CSVs
are processed on the hosting server. Upload caches are scoped to a single
user session; the shared cache contains only the bundled synthetic sample.

Official guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## What Replit means

Replit is a browser-based development environment with cloud execution,
AI coding tools, and hosting. It is an alternative place to develop and host
this Streamlit app. The dashboard is still written in Python using Streamlit,
pandas, and Plotly whichever hosting provider runs it.
