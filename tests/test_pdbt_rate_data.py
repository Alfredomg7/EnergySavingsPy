import unittest
from database.pdbt_rate_data import PdbtRateData
import config

class TestPdbtRateData(unittest.TestCase):
    def setUp(self):
        db_path = config.DATABASE_PATH
        self.end_month = '2022-12'
        self.pdbt_rate_data = PdbtRateData(db_path)
        self.test_data = ['1']
    
    def test_get_charges(self):
        for region_id in self.test_data:
            charges = self.pdbt_rate_data.get_charges(region_id, self.end_month)
            self.assertIsNotNone(charges)
            self.assertIsInstance(charges, list)
            self.assertEqual(len(charges), 12)
            for item in charges:
                self.assertIsInstance(item, dict)

    def test_invalid_region(self):
        self.assertIsNone(self.pdbt_rate_data.get_charges('California', self.end_month))

if __name__ == '__main__':
    unittest.main()
