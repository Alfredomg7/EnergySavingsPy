import unittest
from models.location import Location

class TestLocation(unittest.TestCase):
    def setUp(self):
        self.test_city = 'Mexicali'
        self.invalid_city = 'Atlantis'
        self.location = Location(self.test_city)

    def test_get_region(self):
        # Testing with a valid city
        region = self.location.region
        self.assertIsNotNone(region, f"Region should exist for {self.test_city}")
        self.assertIsInstance(region, str, f"Expected region to be a string for {self.test_city}")

        # Testing with an invalid city
        invalid_location = Location(self.invalid_city)
        region = invalid_location.region
        self.assertIsNone(region, f"Region should be None for an invalid city like {self.invalid_city}")

if __name__ == '__main__':
    unittest.main()