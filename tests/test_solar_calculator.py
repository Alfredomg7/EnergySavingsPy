import unittest
from unittest.mock import Mock
from models.pv_system import PVSystem
from models.rate import Rate
from calculations.solar_calculator import SolarSavingsCalculator

class TestSolarSavingsCalculator(unittest.TestCase):
    def setUp(self):
        self.mock_rate = Mock(spec=Rate)
        self.sample_consumption_data = [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230]
        self.mock_rate.calculate_monthly_payments.return_value = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.sample_consumption_data)

    def test_rate_validation(self):
        invalid_rate = Mock()
        with self.assertRaises(ValueError):
            SolarSavingsCalculator(invalid_rate, self.sample_consumption_data)
    
    def test_pv_system_validation(self):
        invalid_system_size = Mock()
        with self.assertRaises(ValueError):
            self.calculator.calculate_new_monthly_payment(invalid_system_size)
            
    def test_calculate_new_monthly_payment(self):
        mock_pv_system = Mock(spec=PVSystem)
        mock_pv_system.calculate_annual_energy_production.return_value = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        expected_new_monthly_consumption = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
        new_monthly_payment = self.calculator.calculate_new_monthly_payment(mock_pv_system)
        self.mock_rate.calculate_monthly_payments.assert_called_with(expected_new_monthly_consumption)
        expected_new_monthly_payment = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]
        self.assertEqual(new_monthly_payment, expected_new_monthly_payment)

    def test_calculate_new_lifetime_consumption(self):
        mock_pv_system = Mock(spec=PVSystem)
        
        annual_energy_production_deficit = [150 for _ in range(12)]
        start = sum(annual_energy_production_deficit)
        step = 50
        lifetime_production_deficit = [start - i * step for i in range(10) ]
        
        annual_energy_production_surplus = [200 for _ in range(12)]
        start = sum(annual_energy_production_surplus)
        step = 50
        lifetime_production_surplus= [start - i * step for i in range(10) ]

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
