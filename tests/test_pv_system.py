import unittest
from unittest.mock import Mock
from models.location import Location
from models.pv_module import PVModule
from models.pv_system import PVSystem

class TestPVSystem(unittest.TestCase):
    def setUp(self):
        self.pv_module = PVModule(capacity=0.3, tilt_angle=31, efficiency=0.8, lifespan=25, annual_degradation=0.005)
        self.mock_location = Mock(spec=Location)
        self.mock_location.get_solar_hours.return_value = [5, 5.5, 6, 6.5, 7, 7.5, 7, 6.5, 6, 5.5, 5, 4.5]

    def test_valid_initialization(self):
        try:
            PVSystem(pv_module=self.pv_module, pv_module_count=10, efficiency=0.95, location=self.mock_location)
        except ValueError:
            self.fail("Valid initialization raised ValueError unexpectedly!")
    
    def test_invalid_pv_module(self):
        with self.assertRaises(ValueError):
            PVSystem(pv_module="not a pv module", pv_module_count=10, efficiency=0.95, location=self.mock_location)

    def test_invalid_pv_module_count(self):
        with self.assertRaises(ValueError):
            PVSystem(pv_module=self.pv_module, pv_module_count=0, efficiency=0.95, location=self.mock_location)

    def test_invalid_efficiency(self):
        with self.assertRaises(ValueError):
            PVSystem(pv_module=self.pv_module, pv_module_count=10, efficiency=1.5, location=self.mock_location)

    def test_invalid_location(self):
        with self.assertRaises(ValueError):
            PVSystem(pv_module=self.pv_module, pv_module_count=10, efficiency=0.95, location='not a location')

    def test_system_size(self):
        pv_system = PVSystem(pv_module=self.pv_module, pv_module_count=10, efficiency=1, location=self.mock_location)
        expected_size = 3
        actual_size = pv_system.system_size
        self.assertEqual(actual_size, expected_size, msg=f"Expected {expected_size} kW, got {actual_size} kW")

    def test_energy_production(self):
        pv_system = PVSystem(pv_module=self.pv_module, pv_module_count=10, efficiency=1, location=self.mock_location)
        expected_production = [372.00, 369.60, 446.40, 468.00, 520.80, 540.00, 520.80, 483.60, 432.00, 409.20, 360.00, 334.80]
        actual_production = pv_system.calculate_annual_energy_production()
        for expected, actual in zip(expected_production, actual_production):
            self.assertEqual(expected, actual, msg=f"Expected {expected} kWh, got {actual} kwh")
    
    def test_lifetime_production(self):
        pv_system = PVSystem(pv_module=self.pv_module, pv_module_count=10, efficiency=1, location=self.mock_location)
        expected_lifetime_production = [5257.20, 5230.91, 5204.76, 5178.74, 5152.84, 5127.08, 5101.44, 5075.94, 5050.56, 5025.30]
        actual_lifetime_production = pv_system.calculate_lifetime_production()

        for expected, actual in zip(expected_lifetime_production, actual_lifetime_production):
            self.assertEqual(expected, actual, msg=f"Expected {expected}, got {actual}")

if __name__ == '__main__':
    unittest.main()
    