import unittest
from unittest.mock import Mock
from calculations.solar_calculator import SolarSavingsCalculator

class TestSolarSavingsCalculator(unittest.TestCase):
    def setUp(self):
        self.mock_rate = Mock()
        self.sample_consumption_data = [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230]
        self.mock_rate.calculate_monthly_payments.return_value = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.sample_consumption_data)

    def test_calculate_new_monthly_payment(self):
        mock_pv_system = Mock()
        mock_pv_system.calculate_energy_production.return_value = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        expected_new_monthly_consumption = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
        new_monthly_payment = self.calculator.calculate_new_monthly_payment(mock_pv_system)
        self.mock_rate.calculate_monthly_payments.assert_called_with(expected_new_monthly_consumption)
        expected_new_monthly_payment = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]
        self.assertEqual(new_monthly_payment, expected_new_monthly_payment)

if __name__ == '__main__':
    unittest.main()
