import unittest
from unittest.mock import Mock
from models.pv_system import PVModule, PVSystem

class TestPVSystem(unittest.TestCase):
    def setUp(self):
        pv_module = PVModule(capacity=300, tilt_angle=31, efficiency=0.9, lifespan=25, annual_degradation=0.005)
        self.mock_location = Mock()
        self.mock_location.get_solar_hours.return_value = [4.5] * 12
        self.pv_system = PVSystem(pv_module=pv_module, pv_module_count=10, efficiency=0.9, location=self.mock_location)
    
    def test_system_size(self):
        expected_size = 3000
        actual_size = self.pv_system.calculate_system_size()
        self.assertEqual(actual_size, expected_size, msg=f"Expected {expected_size} kW, got {actual_size} kW")


    def test_energy_production(self):
        expected_production = []
        mock_solar_hours = self.mock_location.get_solar_hours()
        for hours in mock_solar_hours:
            monthly_production = self.pv_system.calculate_system_size() * hours * self.pv_system.pv_module.efficiency * self.pv_system.efficiency
            expected_production.append(monthly_production)

        actual_production = self.pv_system.calculate_energy_production()
        for expected, actual in zip(expected_production, actual_production):
            self.assertEqual(expected, actual, msg=f"Expected {expected} kWh, got {actual} kwh")
    
if __name__ == '__main__':
    unittest.main()
    