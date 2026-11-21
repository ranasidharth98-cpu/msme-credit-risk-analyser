import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.risk_metrics import (
    calculate_dscr,
    calculate_monthly_emi,
    classify_dscr_risk_tier,
    report_revenue_drop_stress_test,
)


class TestRiskMetrics(unittest.TestCase):
    def test_emi_known_loan(self):
        """Check EMI for a 12-month loan of 100,000 at 12% annual interest."""
        emi = calculate_monthly_emi(
            loan_amount=100_000,
            annual_interest_rate=12.0,
            tenure_months=12,
        )
        self.assertAlmostEqual(emi, 8884.88, places=2)

    def test_dscr_calculation(self):
        """Check DSCR = (monthly_revenue - monthly_operating_cost) / monthly_emi."""
        dscr = calculate_dscr(
            monthly_revenue=150_000,
            monthly_operating_cost=90_000,
            monthly_emi=30_000,
        )
        self.assertAlmostEqual(dscr, 2.00, places=2)

    def test_risk_tier_boundaries(self):
        """Check High (< 1.0), Medium (1.0 to 1.5), and Low (> 1.5) cut-offs."""
        self.assertEqual(classify_dscr_risk_tier(0.85), "High")
        self.assertEqual(classify_dscr_risk_tier(1.00), "Medium")
        self.assertEqual(classify_dscr_risk_tier(1.50), "Medium")
        self.assertEqual(classify_dscr_risk_tier(1.75), "Low")

    def test_revenue_drop_stress_test_moves_borrower_to_high(self):
        """Check that a 20% revenue drop pushes a Medium borrower into High risk."""
        sample_rows = [
            {
                "borrower_id": "1",
                "monthly_revenue": "100000",
                "monthly_operating_cost": "70000",
                "emi": "25000.00",
                "dscr": "1.20",
                "risk_tier": "Medium",
            }
        ]
        moved = report_revenue_drop_stress_test(sample_rows, revenue_drop_pct=20.0)
        self.assertEqual(moved, 1)


if __name__ == "__main__":
    unittest.main()