import csv
from pathlib import Path


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


def update_borrowers_csv(
    input_path: str | Path = "borrowers.csv",
    output_path: str | Path = "borrowers_with_emi_dscr.csv",
) -> list[dict[str, str]]:
    """Read borrowers.csv, add emi and dscr columns for each row, and write the result."""
    in_path = Path(input_path)
    out_path = Path(output_path)

    with in_path.open(mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        if not reader.fieldnames:
            raise ValueError(f"{in_path} has no header row.")

        # Preserve existing columns and append emi and dscr if not already present
        fieldnames = list(reader.fieldnames)
        for col in ("emi", "dscr"):
            if col not in fieldnames:
                fieldnames.append(col)

        updated_rows: list[dict[str, str]] = []
        for row_num, row in enumerate(reader, start=2):  # row 1 is header
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
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Error processing row {row_num} in {in_path}: {exc}") from exc

            new_row = dict(row)
            new_row["emi"] = f"{emi:.2f}"
            new_row["dscr"] = f"{dscr:.2f}"
            updated_rows.append(new_row)

    with out_path.open(mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"Processed {len(updated_rows)} borrowers -> saved to {out_path}")
    return updated_rows


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent  # C:\Users\sidha\Documents\msme-credit-risk-analyser

    update_borrowers_csv(
        project_root / "data" / "borrowers.csv",
        output_path=project_root / "borrowers_with_emi_dscr.csv",
    )