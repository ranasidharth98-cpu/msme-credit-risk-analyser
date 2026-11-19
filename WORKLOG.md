\# Work log





\## 2026-11-19 (Thursday)

\*\*Added:\*\* 

\--EMI and DSCR calculation in risk\_metrics.py, 

\*\*Learned:\*\*

\--Dataset Update (data/borrowers.csv): Updated the Day 1 borrower generation logic (preserving SEED = 42) to include monthly\_operating\_cost as a 0.60 to 0.95 share of monthly\_revenue.

\--CSV Pipeline (src/risk\_metrics.py): Linked calculate\_monthly\_emi and calculate\_dscr to data/borrowers.csv using csv.DictReader, csv.DictWriter, and pathlib.Path relative to the project root, outputting emi and dscr columns across all 200 borrowers.

\*\*Next:\*\*

\-Risk tiers and Portfolio summary



