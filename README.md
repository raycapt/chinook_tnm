
# Voyage Performance Report (Streamlit)

Interactive report to compare Pre-DD vs Post-DD performance under B.c / L.c and across any `t/1000nm*` metric.

## Local run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud
- Push this folder to GitHub.
- In Streamlit Cloud, set the repo and choose **app.py** as the main file.
- The app will use `data/voyage_data.csv` if present or fall back to embedded sample data.
- You can upload your own CSV/TSV in the sidebar to refresh.

## Data format
Expected columns (exact names):
- `Voy no`, `Pre-DD / Post-DD`, `B/L`, `Combined`, `Avg Draft`, `Cargo Qty`, `EOSP Date`, `Dur (COSP-EOSP) (Hrs)`, `NM`, `ME FO`, `ME GO`, `AE FO`, `AE GO`, `ME+AE`, `Blr`, 
- All the `t/1000nm(...)` columns,
- `From`, `To`.

## Features
- Filter by **Phase (Pre-DD/Post-DD)** and **Combined (B.c/L.c)**
- Select any **t/1000nm** metric
- Multi-select voyages to compare
- Averages table by Phase vs Combined
- **Improvement** table: Post vs Pre (Δ and % change; lower is better)
- Download current or filtered data as CSV
