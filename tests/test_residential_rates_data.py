import unittest
from database.residential_rates_data import ResidentialRatesData
from utils.date_utils import extract_month
import config

class TestResidentialRatesData(unittest.TestCase):
    def setUp(self):
        self.db_path = config.DATABASE_PATH
        self.residential_rates_data = ResidentialRatesData(self.db_path)
        self.test_rate = '1F'
        self.summer_months = [5, 6, 7, 8, 9, 10]
        self.winter_months = [11, 12, 1, 2, 3, 4]
        self.end_year_month = '2024-12'

    def _test_get_summer_charges(self):
        charges = self.residential_rates_data._get_summer_charges(
            self.test_rate, self.summer_months, self.end_year_month
        )
        self.assertIsNotNone(charges)
        self.assertIsInstance(charges, list)
        self.assertEqual(len(charges), 6)
        self.assertTrue(all(isinstance(charge, dict) for charge in charges))

    def _test_get_winter_charges(self):
        charges = self.residential_rates_data._get_winter_charges(
            self.test_rate, self.winter_months, self.end_year_month
        )
        self.assertIsNotNone(charges)
        self.assertIsInstance(charges, list)
        self.assertEqual(len(charges), 6)
        self.assertTrue(all(isinstance(charge, dict)) for charge in charges)

    def test_get_charges(self):
        all_charges = self.residential_rates_data.get_charges(
            self.test_rate, self.summer_months, self.winter_months, self.end_year_month
        )
        self.assertIsNotNone(all_charges)
        self.assertIsInstance(all_charges, list)
        self.assertEqual(len(all_charges), 12)
        self.assertTrue(all(isinstance(charge, dict)) for charge in all_charges)
        
        months = [extract_month(charge['billing_period']) for charge in all_charges]
        expected_order = sorted(self.winter_months + self.summer_months)
        self.assertListEqual(months, expected_order)