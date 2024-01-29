import unittest
from unittest.mock import Mock
from models.pv_system import PVModule, PVSystem
from calculations.solar_calculator import SolarSavingsCalculator

class TestSolarSavingsCalculator(unittest.TestCase):
    def setUp(self):
        self.mock_pv_module = PVModule(capacity=0.3, tilt_angle=31, efficiency=0.8, lifespan=25, annual_degradation=0.005)
        self.mock_location = Mock()
        self.mock_location.get_solar_hours.return_value = [150, 165, 180, 195, 210, 225, 210, 195, 180, 165, 150, 135]
        self.pv_system = PVSystem(self.mock_pv_module, pv_module_count=10, efficiency=1, location=self.mock_location)
        self.rate = 0.12
        self.sample_consumption_data = [177, 181, 248, 354, 548, 1185, 1280, 1280, 478, 227, 204, 365]
        self.calculator = SolarSavingsCalculator(self.rate, self.sample_consumption_data)

    def test_new_monthly_consumption(self):
        expected_new_monthly_consumption = [0, 0, 0, 0, 0, 0, 485.00, 812.00, 46.00, 0, 0, 0]
        actual_new_monthly_consumption = self.calculator.calculate_new_monthly_consumption(self.pv_system)
        self.assertEqual(expected_new_monthly_consumption, actual_new_monthly_consumption, f"Expected {expected_new_monthly_consumption}, got {actual_new_monthly_consumption}")