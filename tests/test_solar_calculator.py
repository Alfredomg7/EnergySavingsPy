import unittest
from unittest.mock import Mock
from models.pv_system import PVModule, PVSystem
from calculations.solar_calculator import SolarSavingsCalculator

class TestSolarSavingsCalculator(unittest.TestCase):
    def setUp(self):
        self.mock_pv_module = PVModule(capacity=300, tilt_angle=31, efficiency=0.9, lifespan=25, annual_degradation=0.005)
        self.mock_location = Mock()
        self.mock_location.get_solar_hours.return_value = [5, 5.5, 6, 6.5, 7, 7.5, 7, 6.5, 6, 5.5, 5, 4.5]
        self.pv_system = PVSystem(self.mock_pv_module, pv_module_count=10, efficiency=0.9, location=self.mock_location)
        self.rate = 0.12
        self.sample_consumption_data = [50000, 45000, 60000, 55000, 50000, 45000, 5000, 5500, 6000, 5500, 50000, 45000]
        self.calculator = SolarSavingsCalculator(self.rate, self.sample_consumption_data)

    def test_new_monthly_consumption(self):
        expected_new_monthly_consumption = [37850, 31635, 45420, 39205, 32990, 26775, 0, 0, 0, 0, 37850, 34065]
        actual_new_monthly_consumption = self.calculator.calculate_new_monthly_consumption(self.pv_system)
        self.assertEqual(expected_new_monthly_consumption, actual_new_monthly_consumption, f"Expected {expected_new_monthly_consumption}, got {actual_new_monthly_consumption}")