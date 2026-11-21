import csv
from pathlib import Path

import pandas as pd


def calculate_monthly_emi(loan_amount: float, annual_interest_rate: float, tenure_months: int) -> float:
    """Calculate and return the Equated Monthly Instalment (EMI)."""
    if loan_amount <= 0 or tenure_months <= 0:
        raise ValueError("loan_amount and tenure_months must be greater than 0.")
    if annual_interest_rate < 0:
        raise ValueError("annual_interest_rate cannot be negative.")

    if annual_interest_rate == 0:
        return loan_amount / tenure_months

    monthly_rate = (annual_interest_rate / 100) / 12
    growth_factor = (1 + monthly_rate) ** tenure_months
    return loan_amount * monthly_rate * growth_factor / (growth_factor - 1)


def calculate_dscr(monthly_revenue: float, monthly_operating_cost: float, monthly_emi: float) -> float:
    """Calculate Debt Service Coverage Ratio (DSCR) for a borrower."""
    if monthly_emi <= 0:
        raise ValueError("monthly_emi must be greater than 0.")

    net_operating_income = monthly_revenue - monthly_operating_cost
    return net_operating_income / monthly_emi


def classify_dscr_risk_tier(dscr: float) -> str:
    """Map a DSCR value to Low, Medium, or High risk."""
    if dscr < 1.0:
        return "High"
    if dscr <= 1.5:
        return "Medium"
    return "Low"


def print_risk_summary_table(rows: list[dict[str, str]]) -> None:
    """Print a formatted summary table of borrower counts and percentages by risk tier."""
    total = len(rows)
    counts = {"High": 0, "Medium": 0, "Low": 0}

    for row in rows:
        tier = row.get("risk_tier", "")
        if tier in counts:
            counts[tier] += 1

    print("\n=== DSCR Risk Tier Summary ===")
    print(f"{'Risk Tier':<10} {'Borrowers':>10} {'Share':>10}")
    print("-" * 32)
    for tier in ("High", "Medium", "Low"):
        count = counts[tier]
        pct = (count / total * 100) if total > 0 else 0.0
        print(f"{tier:<10} {count:>10} {pct:>9.1f}%")
    print("-" * 32)
    print(f"{'Total':<10} {total:>10} {'100.0%' if total > 0 else '0.0%':>10}\n")


def print_pandas_summaries(rows: list[dict[str, str]]) -> None:
    """Print borrower count and total loan amount grouped by risk_tier and sector."""
    if not rows:
        print("\nNo borrower rows available for summary tables.\n")
        return

    df = pd.DataFrame(rows)
    df["loan_amount_num"] = pd.to_numeric(df["loan_amount"], errors="coerce")

    tier_summary = (
        df.groupby("risk_tier", dropna=False)
        .agg(
            borrowers=("borrower_id", "count"),
            total_loan_amount=("loan_amount_num", "sum"),
        )
        .reindex(["High", "Medium", "Low"])
        .dropna(how="all")
    )
    tier_summary["borrowers"] = tier_summary["borrowers"].fillna(0).astype(int)
    tier_summary["total_loan_amount"] = tier_summary["total_loan_amount"].fillna(0).round(2)

    sector_summary = (
        df.groupby("sector", dropna=False)
        .agg(
            borrowers=("borrower_id", "count"),
            total_loan_amount=("loan_amount_num", "sum"),
        )
        .sort_values("total_loan_amount", ascending=False)
    )
    sector_summary["borrowers"] = sector_summary["borrowers"].astype(int)
    sector_summary["total_loan_amount"] = sector_summary["total_loan_amount"].round(2)

    print("=== Loan Exposure by Risk Tier ===")
    print(tier_summary.to_string())

    print("\n=== Loan Exposure by Sector ===")
    print(sector_summary.to_string())
    print()

def report_revenue_drop_stress_test(
        rows: list[dict[str, str]],
    revenue_drop_pct: float = 20.0,
) ->int:
    """Recalculate DSCR after a revenue drop and report how many borrowers move into High tier."""
    multiplier = 1.0 -(revenue_drop_pct / 100.0)
    moved_into_high = 0
    already_high = 0
    stressed_high_total = 0

    for row in rows:
        base_tier = row["risk_tier"]
        stressed_revenue = float(row["monthly_revenue"])*multiplier
        monthly_operating_cost = float(row["monthly_operating_cost"])
        emi = float(row["emi"])

        stressed_dscr = calculate_dscr(
            monthly_revenue=stressed_revenue,
            monthly_operating_cost=monthly_operating_cost,
            monthly_emi=emi,
        )
        stressed_tier = classify_dscr_risk_tier(stressed_dscr)

        if stressed_tier =="High":
            stressed_high_total += 1
            if base_tier == "High":
                already_high += 1
            else:
                moved_into_high += 1

    print(f"=== Stress Test: {revenue_drop_pct:.0f}% Revenue Drop ===")
    print(f"Already in High risk tier:            {already_high}")
    print(f"Newly moved into High risk tier:      {moved_into_high}")
    print(f"Total borrowers in High risk tier:    {stressed_high_total}\n")
    return moved_into_high

def update_borrowers_csv(
    input_path: str | Path = "borrowers.csv",
    output_path: str | Path = "borrowers_with_emi_dscr.csv",
) -> list[dict[str, str]]:
    """Read borrowers.csv, add emi, dscr, and risk_tier columns, write output, and print summaries."""
    in_path = Path(input_path)
    out_path = Path(output_path)

    with in_path.open(mode="r", newline="", encoding="utf-8-sig") as infile:
        reader = csv.DictReader(infile)
        if not reader.fieldnames:
            raise ValueError(f"{in_path} has no header row.")

        fieldnames = list(reader.fieldnames)
        for col in ("emi", "dscr", "risk_tier"):
            if col not in fieldnames:
                fieldnames.append(col)

        updated_rows: list[dict[str, str]] = []
        for row_num, row in enumerate(reader, start=2):
            try:
                emi = calculate_monthly_emi(
                    loan_amount=float(row["loan_amount"]),
                    annual_interest_rate=float(row["annual_interest_rate"]),
                    tenure_months=int(float(row["tenure_months"])),
                )
                dscr = calculate_dscr(
                    monthly_revenue=float(row["monthly_revenue"]),
                    monthly_operating_cost=float(row["monthly_operating_cost"]),
                    monthly_emi=emi,
                )
                risk_tier = classify_dscr_risk_tier(dscr)
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Error processing row {row_num} in {in_path}: {exc}") from exc

            new_row = dict(row)
            new_row["emi"] = f"{emi:.2f}"
            new_row["dscr"] = f"{dscr:.2f}"
            new_row["risk_tier"] = risk_tier
            updated_rows.append(new_row)

    with out_path.open(mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"Processed {len(updated_rows)} borrowers -> saved to {out_path}")
    print_risk_summary_table(updated_rows)
    print_pandas_summaries(updated_rows)
    report_revenue_drop_stress_test(updated_rows, revenue_drop_pct=20.0)
    return updated_rows


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    update_borrowers_csv(
        input_path=project_root / "data" / "borrowers.csv",
        output_path=project_root / "borrowers_with_emi_dscr.csv",
    )