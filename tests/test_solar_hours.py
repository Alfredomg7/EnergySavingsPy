import os
import unittest
from database.solar_hours_data import SolarHoursData
from models.location import Location
import config

class TestSolarHours(unittest.TestCase):
    def setUp(self):
        db_path = config.DATABASE_PATH
        print(f"Using database path: {db_path}")
        self.solar_hours_data = SolarHoursData(db_path)

        self.test_data = {
            'Mexicali': [17, 32, 47],
            'San Felipe': [16, 31, 46]
        }
    
    def test_solar_hours(self):
        for city, tilts in self.test_data.items():
            location = Location(city, self.solar_hours_data)
            for tilt in tilts:
                solar_hours = location.get_solar_hours(tilt)
                self.assertIsNotNone(solar_hours, f"Data should exist for {city} with tilt {tilt}°")
        
    def test_invalid_inputs(self):
        non_existing_location = Location("Borderland", self.solar_hours_data)
        self.assertIsNone(non_existing_location.get_solar_hours(15))

        invalid_tilt_location = Location("San Felipe", self.solar_hours_data)
        self.assertIsNone(invalid_tilt_location.get_solar_hours(999))


if __name__ == '__main__':
    unittest.main()