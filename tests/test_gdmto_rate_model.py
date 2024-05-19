import unittest
from unittest.mock import Mock, patch
from models.gdmto_rate import GdmtoRate
from models.location import Location

class TestGdmtoRate(unittest.TestCase):
    def setUp(self):
        self.state = 'Baja California'
        self.end_month = '2024-04'
        self.location = Mock(spec=Location)
        self.location.region_id = 1
        self.mock_charges = [{'transmission': 0.1, 'distribution': 100, 'cenace': 0.01,
                            'supplier': 500, 'services': 0.02, 'energy': 0.07, 'capacity': 300} for _ in range(12)]

    def test_calculate_monthly_payments(self):
        with patch('models.gdmto_rate.CommercialRatesData.get_charges', return_value=self.mock_charges):
            gdmto_rate = GdmtoRate(self.location, self.end_month)
            monthly_consumptions = [500 * (i + 1) for i in range(12)]
            monthly_demands = [10 for _ in range(12)]
            monthly_power_factors = [96 - i for i in range(12)]
            monthly_payments = gdmto_rate.calculate_monthly_payments(monthly_consumptions, demand=monthly_demands, power_factor=monthly_power_factors)
            expected_payments = [1194.81, 1876.12, 2486.85, 3135.80, 3875.94, 4444.45 , 5232.18, 5795.25, 6379.74, 7231.35, 7524.69, 8277.78]
            self.assertIsInstance(monthly_payments, list)
            self.assertEqual(len(monthly_payments), 12)                
            self.assertEqual(monthly_payments, expected_payments)
    
    def test_calculate_demand(self):
        gdmto_rate = GdmtoRate(self.location, self.end_month)
        consumptions = [1000 *(i + 1) for i in range(12)]
        days_in_months = [31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 31, 30]

        expected_demands = [2.44, 5.05, 7.33, 9.78, 12.63, 14.66, 17.68, 19.55, 21.99, 26.12, 26.88, 30.30]

        for consumption, expected_demand, days_in_month in zip(consumptions, expected_demands, days_in_months):
            self.assertEqual(gdmto_rate._calculate_demand(consumption, days_in_month), expected_demand)

    def test_calculate_power_factor_rate(self):
        gdmto_rate = GdmtoRate(self.location, self.end_month)
        power_factors = [100, 95, 90, 85, 80]
        expected_charges = [-0.025, -0.013157, 0, 0.0353, 0.075]

        for power_factor, expected_charge in zip(power_factors, expected_charges):
            self.assertAlmostEqual(gdmto_rate._calculate_power_factor_rate(power_factor), expected_charge, places=4)

if __name__ == "__main__":
    unittest.main()
