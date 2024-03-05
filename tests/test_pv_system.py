import unittest
from unittest.mock import Mock
from models.pv_module import PVModule
from models.pv_system import PVSystem

class TestPVSystem(unittest.TestCase):
    def setUp(self):
        pv_module = PVModule(capacity=0.3, tilt_angle=31, efficiency=0.8, lifespan=25, annual_degradation=0.005)
        self.mock_location = Mock()
        self.mock_location.get_solar_hours.return_value = [5, 5.5, 6, 6.5, 7, 7.5, 7, 6.5, 6, 5.5, 5, 4.5]
        self.pv_system = PVSystem(pv_module=pv_module, pv_module_count=10, efficiency=1, location=self.mock_location)
    
    def test_system_size(self):
        expected_size = 3
        actual_size = self.pv_system.calculate_system_size()
        self.assertEqual(actual_size, expected_size, msg=f"Expected {expected_size} kW, got {actual_size} kW")


    def test_energy_production(self):
        expected_production = [372.00, 369.60, 446.40, 468.00, 520.80, 540.00, 520.80, 483.60, 432.00, 409.20, 360.00, 334.80]
        actual_production = self.pv_system.calculate_energy_production()
        for expected, actual in zip(expected_production, actual_production):
            self.assertEqual(expected, actual, msg=f"Expected {expected} kWh, got {actual} kwh")
    
if __name__ == '__main__':
    unittest.main()
    