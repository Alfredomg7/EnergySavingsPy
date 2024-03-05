import unittest
from models.pv_module import PVModule

class TestPVModule(unittest.TestCase):

    def test_valid_initialization(self):
        try:
            PVModule(0.5, 45, 0.15, 20, 0.005)
        except ValueError:
            self.fail("Valid initialization raised ValueError")
    
    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            PVModule(0, 45, 0.15)  
        with self.assertRaises(ValueError):
            PVModule(1.5, 45, 0.15)

    def test_invalid_tilt_angle(self):
        with self.assertRaises(ValueError):
            PVModule(0.5, -1, 0.15)
        with self.assertRaises(ValueError):
            PVModule(0.5, 91, 0.15)

    def test_invalid_efficiency(self):
        with self.assertRaises(ValueError):
            PVModule(0.5, 45, 0)
        with self.assertRaises(ValueError):
            PVModule(0.5, 45, 1.1)

    def test_invalid_lifespan(self):
        with self.assertRaises(ValueError):
            PVModule(0.5, 45, 0.15, 0)
        with self.assertRaises(ValueError):
            PVModule(0.5, 45, 0.15, 31)
        with self.assertRaises(ValueError):
            PVModule(0.5, 45, 0.15, 20.5)

    def test_invalid_annual_degradation(self):
        with self.assertRaises(ValueError):
            PVModule(0.5, 45, 0.15, 25, -0.01)
        with self.assertRaises(ValueError):
            PVModule(0.5, 45, 0.15, 25, 0.11)

if __name__ == '__main__':
    unittest.main()