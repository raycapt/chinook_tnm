
Voyage Performance App — Quick Start

1) Download both files:
   - voyage_data.csv
   - voyage_performance_app.py

2) In a terminal:
   pip install streamlit pandas matplotlib

3) Run the app:
   streamlit run voyage_performance_app.py

4) Use the sidebar to:
   - Filter by Phase (Pre-DD / Post-DD)
   - Filter by Combined (B.c / L.c)
   - Pick voyages to compare
   - Choose any t/1000nm metric (e.g., Total ME+AE, AE-FO, etc.)

5) Update Data:
   - Either upload a CSV/TSV directly in the app (same columns), or
   - Replace voyage_data.csv and rerun.
