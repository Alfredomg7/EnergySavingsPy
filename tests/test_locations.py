import unittest
from models.location import Location

class TestLocation(unittest.TestCase):
    def setUp(self):
        self.valid_city = 'Mexicali'
        self.invalid_city = 'Atlantis'
        self.valid_location = Location(self.valid_city)
        self.invalid_location = Location(self.invalid_city)

    def test_get_region(self):
        region = self.valid_location.region
        self.assertIsNotNone(region)
        self.assertIsInstance(region, str)
        self.assertEqual(region,'Baja California')

        region = self.invalid_location.region
        self.assertIsNone(region)

    def test_get_region_id(self):
        region_id = self.valid_location.region_id
        self.assertIsNotNone(region_id)
        self.assertIsInstance(region_id, str)
        self.assertEqual(region_id, '1')

        region_id = self.invalid_location.region
        self.assertIsNone(region_id)

    def test_get_residential_rate(self):
        residential_rate = self.valid_location.residential_rate
        self.assertIsNotNone(residential_rate)
        self.assertIsInstance(residential_rate, str)
        self.assertEqual(residential_rate, '1F')

    def test_get_summer_start_month(self):
        summer_start_month = self.valid_location.summer_start_month
        self.assertIsNotNone(summer_start_month)
        self.assertIsInstance(summer_start_month, int)
        self.assertEqual(summer_start_month, 5)

        summer_start_month = self.invalid_location.summer_start_month
        self.assertIsNone(summer_start_month)
        
if __name__ == '__main__':
    unittest.main()