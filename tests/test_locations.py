import unittest
from models.location import Location

class TestLocation(unittest.TestCase):
    def setUp(self):
        self.valid_cities = {'San Felipe': '1F', 'Mexicali': '1F', 'Tijuana': '1A'}
        self.invalid_city = 'Atlantis'
        self.invalid_location = Location(self.invalid_city)

    def test_get_region(self):
        for city in self.valid_cities.keys():
            location = Location(city)
            region = location.region
            self.assertIsNotNone(region)
            self.assertIsInstance(region, str)
            self.assertEqual(region, 'Baja California')

        region = self.invalid_location.region
        self.assertIsNone(region)

    def test_get_region_id(self):
        for city in self.valid_cities.keys():
            location = Location(city)
            region_id = location.region_id
            self.assertIsNotNone(region_id)
            self.assertIsInstance(region_id, str)
            self.assertEqual(region_id, '1')

        region_id = self.invalid_location.region
        self.assertIsNone(region_id)

    def test_get_residential_rate(self):
        for city, expected_rate in self.valid_cities.items():
            location = Location(city)
            actual_rate = location.residential_rate
            self.assertIsNotNone(actual_rate)
            self.assertIsInstance(actual_rate, str)
            self.assertEqual(actual_rate, expected_rate)

    def test_get_summer_start_month(self):
        for city in self.valid_cities.keys():
            location = Location(city)
            summer_start_month = location.summer_start_month
            self.assertIsNotNone(summer_start_month)
            self.assertIsInstance(summer_start_month, int)
            self.assertEqual(summer_start_month, 5)

        summer_start_month = self.invalid_location.summer_start_month
        self.assertIsNone(summer_start_month)
        
if __name__ == '__main__':
    unittest.main()
