import unittest
from database.commercial_rates_data import CommercialRatesData
import config

class TestCommercialRatesData(unittest.TestCase):
    def setUp(self):
        db_path = config.DATABASE_PATH
        self.end_month = '2024-03'
        self.region_id = 1
        self.pdbt_rate_data = CommercialRatesData('PDBT', db_path)
        self.gdmto_rate_data = CommercialRatesData('GDMTO', db_path)
    
    def test_get_pdbt_charges(self):
        charges = self.pdbt_rate_data.get_charges(self.region_id, self.end_month)
        self.assertIsNotNone(charges)
        self.assertIsInstance(charges, list)
        self.assertEqual(len(charges), 12)
        for item in charges:
            self.assertIsInstance(item, dict)

    def test_get_pdbt_charges(self):
        charges = self.gdmto_rate_data.get_charges(self.region_id, self.end_month)
        self.assertIsNotNone(charges)
        self.assertIsInstance(charges, list)
        self.assertEqual(len(charges), 12)
        for item in charges:
            self.assertIsInstance(item, dict)

    def test_invalid_region_id(self):
        self.assertIsNone(self.pdbt_rate_data.get_charges(99, self.end_month))

    def test_invalid_rate(self):
        invalid_rate_data = CommercialRatesData('ABCD', config.DATABASE_PATH)
        self.assertIsNone(invalid_rate_data.get_charges(1, self.end_month))
    
    def test_invalid_end_month(self):
        self.assertIsNone(self.gdmto_rate_data.get_charges(1, '2030-12'))
        with self.assertRaises(ValueError):
            self.gdmto_rate_data.get_charges(1, '2024-March')

if __name__ == '__main__':
    unittest.main()
