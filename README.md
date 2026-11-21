MSME CREDIT RISK ANALYSER

A Python credit risk assessment pipeline for **Micro, Small, and Medium Enterprises (MSMEs)**. It computes **Equated Monthly Instalments (EMI)** and **Debt Service Coverage Ratio (DSCR)**, classifies borrowers into risk tiers, generates portfolio summaries with `pandas`, runs a **20% revenue-drop stress test**, and verifies calculations with `unittest`.

---

## Why This Project Matters

Small businesses are the backbone of local economies, yet small revenue dips can quickly squeeze their ability to service monthly debt. This project models how a lender or risk analyst can:
* Measure monthly repayment obligations (**EMI**) against operating cash flow (**DSCR**).
* Spot vulnerable borrowers early using clear DSCR cut-offs.
* Test portfolio resilience under a **20% revenue shock** and count how many borrowers slip into the **High** risk tier.

---

## What It Does

* **EMI Calculation:** Computes the fixed monthly instalment from loan principal, annual interest rate, and tenure in months.
* **DSCR Calculation:** Evaluates repayment coverage.
* **Risk-Tier Classification & CSV Export:** Labels each borrower as **High**, **Medium**, or **Low** risk and writes the results to `borrowers_with_emi_dscr.csv`.
* **Portfolio Summaries:** Uses `pandas` `groupby` to summarize borrower counts and total loan exposure across risk tiers and business sectors.
* **20% Revenue-Drop Stress Test:** Recalculates DSCR assuming a **20% drop in monthly revenue** and reports how many borrowers newly move into the **High** risk tier.
* **Automated Unit Tests:** Validates core formulas, risk-tier boundaries, and stress-test migration logic via Python's built-in `unittest` framework.

---

## Risk-Tier Rules

| Risk Tier | DSCR Cut-Off | What It Means |
| :--- | :--- | :--- |
| **High** | `< 1.00` | Cash left after operating costs is less than the monthly EMI obligation. |
| **Medium** | `1.00` to `1.50` | Cash flow covers the monthly EMI with a moderate buffer. |
| **Low** | `> 1.50` | Strong repayment cushion (`1.5x` EMI or higher). |

---

## How to run this program
1.Open Command Prompt (CMD) inside the msme-credit-risk-analyser project folder.
2.Install required dependencies (if not already installed) by running pip install pandas.
3.Run python src\risk_metrics.py to calculate EMI, DSCR, risk tiers, summaries, and the 20% revenue-drop stress test.
4.Check borrowers_with_emi_dscr.csv in the project folder for the generated borrower risk results.
5.Run python tests\test_risk_metrics.py -v to verify all unit tests pass.
