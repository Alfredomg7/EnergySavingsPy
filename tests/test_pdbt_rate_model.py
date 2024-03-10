import unittest
from unittest.mock import patch
from models.pdbt_rate import PdbtRate

class TestPdbtRate(unittest.TestCase):
    def setUp(self):
        self.state = 'Baja California'
        self.end_month = '2022-12'

        self.mock_charges = [{'transmission': 0.1, 'distribution': 0.05, 'cenace': 0.01,
                            'supplier': 100, 'services': 0.02, 'energy': 0.07, 'capacity': 0.03} for _ in range(12)]

    def test_fix_charge(self):
        with patch('models.pdbt_rate.PdbtRateData.get_charges', return_value=self.mock_charges):
            pdbt_rate = PdbtRate(self.state, self.end_month)

            self.assertEqual(pdbt_rate.fix_charge, 1296.0)

    def test_calculate_monthly_payments(self):
        with patch('models.pdbt_rate.PdbtRateData.get_charges', return_value=self.mock_charges):
            pdbt_rate = PdbtRate(self.state, self.end_month)
            start = 100
            step = 50
            months = 12
            monthly_consumptions = [start + i * step for i in range(months)]
            monthly_payments = pdbt_rate.calculate_monthly_payments(monthly_consumptions)

            self.assertIsInstance(monthly_payments, list)
            self.assertEqual(len(monthly_payments), 12)

            for i, consumption in enumerate(monthly_consumptions):
                expected_payment = sum([
                    consumption * 0.1, consumption * 0.05, consumption * 0.01, 
                    100, consumption * 0.02, consumption * 0.07, consumption * 0.03
                ]) * 1.08
                self.assertEqual(monthly_payments[i], round(expected_payment,2))

if __name__ == "__main__":
    unittest.main()
