\# Work log





\## 2026-11-19 (Thursday)

\*\*Added:\*\* 

\--EMI and DSCR calculation in risk\_metrics.py, 

\*\*Learned:\*\*

\--Dataset Update (data/borrowers.csv): Updated the Day 1 borrower generation logic (preserving SEED = 42) to include monthly\_operating\_cost as a 0.60 to 0.95 share of monthly\_revenue.

\--CSV Pipeline (src/risk\_metrics.py): Linked calculate\_monthly\_emi and calculate\_dscr to data/borrowers.csv using csv.DictReader, csv.DictWriter, and pathlib.Path relative to the project root, outputting emi and dscr columns across all 200 borrowers.

\*\*Next:\*\*

\-Risk tiers and Portfolio summary

## 2026-11-20 (Friday)
**Added:**
Risk Tier Classification (src/risk_metrics.py): Implemented classify_dscr_risk_tier and wrote the risk_tier column into borrowers_with_emi_dscr.csv.
Summary Tables: Built summary output showing borrower counts and shares by risk tier, plus pandas groupby summaries for borrower count and total loan amount grouped by risk_tier and sector.




