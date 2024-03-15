import unittest
from database.pdbt_rate_data import PdbtRateData
import config

class TestPdbtRateData(unittest.TestCase):
    def setUp(self):
        db_path = config.DATABASE_PATH
        self.start_month = '2022-01'
        self.end_month = '2022-12'
        self.pdbt_rate_data = PdbtRateData(db_path)
        self.test_data = [1]
    
    def test_get_charges(self):
        for region_id in self.test_data:
            charges = self.pdbt_rate_data.get_charges(region_id, self.start_month, self.end_month)
            self.assertIsNotNone(charges, f"Data should exist for region with ID: {region_id}")
            self.assertIsInstance(charges, list, f"Expected charges to be a list for region with ID: {region_id}")
            self.assertEqual(len(charges), 12, f"Expected 12 months of charges data for region with ID: {region_id}")
            for item in charges:
                self.assertIsInstance(item, dict, f"Expected each charge to be a dictionary for region with ID: {region_id}")

    def test_invalid_region(self):
        self.assertIsNone(self.pdbt_rate_data.get_charges('California', self.start_month, self.end_month))

if __name__ == '__main__':
    unittest.main()
