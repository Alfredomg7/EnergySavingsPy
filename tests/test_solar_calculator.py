import unittest
from unittest.mock import Mock
from models.pv_system import PVSystem
from models.rate import Rate
from calculations.solar_calculator import SolarSavingsCalculator

class TestSolarSavingsCalculator(unittest.TestCase):
    def setUp(self):
        self.mock_rate = Mock(spec=Rate)
        start = 120
        step = 10
        self.months = 12
        self.sample_consumption_data = [start + i * step for i in range(self.months)]
        start = 100
        self.mock_rate.calculate_monthly_payments.return_value = [start + i * step for i in range(self.months)]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.sample_consumption_data)

    def test_rate_validation(self):
        invalid_rate = Mock()
        with self.assertRaises(ValueError):
            SolarSavingsCalculator(invalid_rate, self.sample_consumption_data)
    
    def test_pv_system_validation(self):
        invalid_system_size = Mock()
        with self.assertRaises(ValueError):
            self.calculator.calculate_new_monthly_payment(invalid_system_size)

    def test_calculate_monthly_energy_savings(self):
        mock_pv_system = Mock(spec=PVSystem)
        monthly_production_deficit = [100 for _ in range(self.months)]
        monthly_production_surplus = [170 for _ in range(self.months)]

        mock_pv_system.calculate_annual_energy_production.return_value = monthly_production_deficit
        expected_monthly_energy_savings = monthly_production_deficit
        actual_monthly_energy_savings = self.calculator.calculate_monthly_energy_savings(mock_pv_system)
        self.assertEqual(actual_monthly_energy_savings, expected_monthly_energy_savings)

        mock_pv_system.calculate_annual_energy_production.return_value = monthly_production_surplus
        expected_monthly_energy_savings = [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 170]
        actual_monthly_energy_savings = self.calculator.calculate_monthly_energy_savings(mock_pv_system)
        self.assertEqual(actual_monthly_energy_savings, expected_monthly_energy_savings)

    def test_calculate_new_monthly_payment(self):
        mock_pv_system = Mock(spec=PVSystem)
        annual_energy_production_deficit = [100 for _ in range(self.months)]
        annual_energy_production_surplus = [300 for _ in range(self.months)]

        mock_pv_system.calculate_annual_energy_production.return_value = annual_energy_production_deficit
        start = 20
        step = 10 
        expected_new_monthly_consumption_deficit = [start + i * step for i in range(self.months)]
        self.mock_rate.calculate_monthly_payments.return_value = expected_new_monthly_consumption_deficit
        new_monthly_payment_deficit = self.calculator.calculate_new_monthly_payment(mock_pv_system)
        self.mock_rate.calculate_monthly_payments.assert_called_with(expected_new_monthly_consumption_deficit)
        self.assertEqual(new_monthly_payment_deficit, expected_new_monthly_consumption_deficit)

        mock_pv_system.calculate_annual_energy_production.return_value = annual_energy_production_surplus
        expected_new_monthly_consumption_surplus = [0 for _ in range(self.months)]
        expected_new_monthly_payment_surplus = [0 for _ in range(self.months)] 
        self.mock_rate.calculate_monthly_payments.return_value = expected_new_monthly_payment_surplus
        new_monthly_payment_surplus = self.calculator.calculate_new_monthly_payment(mock_pv_system)
        self.mock_rate.calculate_monthly_payments.assert_called_with(expected_new_monthly_consumption_surplus)
        self.assertEqual(new_monthly_payment_surplus, expected_new_monthly_payment_surplus)

    def test_calculate_new_lifetime_consumption(self):
        mock_pv_system = Mock(spec=PVSystem)
        step = 50
        years = 10

        annual_energy_production_deficit = [150 for _ in range(self.months)]
        start = sum(annual_energy_production_deficit)
        lifetime_production_deficit = [start - i * step for i in range(years) ]
        
        annual_energy_production_surplus = [200 for _ in range(self.months)]
        start = sum(annual_energy_production_surplus)
        lifetime_production_surplus= [start - i * step for i in range(years) ]

        mock_pv_system.calculate_annual_energy_production.return_value = annual_energy_production_deficit
        mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_deficit
        expected_consumption_deficit = [sum(self.sample_consumption_data) - production for production in lifetime_production_deficit]
        actual_consumption_deficit = self.calculator.calculate_new_lifetime_consumption(mock_pv_system)
        self.assertEqual(actual_consumption_deficit, expected_consumption_deficit)

        mock_pv_system.calculate_annual_energy_production.return_value = annual_energy_production_surplus
        mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_surplus
        expected_consumption_surplus = [max(sum(self.sample_consumption_data) - production, 0) for production in lifetime_production_surplus]
        actual_consumption_surplus = self.calculator.calculate_new_lifetime_consumption(mock_pv_system)
        self.assertEqual(actual_consumption_surplus, expected_consumption_surplus)

if __name__ == '__main__':
    unittest.main()
