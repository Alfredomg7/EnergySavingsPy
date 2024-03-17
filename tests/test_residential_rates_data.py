import unittest
from database.residential_rates_data import ResidentialRatesData
from utils.date_utils import format_month
import config

class TestResidentialRatesData(unittest.TestCase):
    def setUp(self):
        self.db_path = config.DATABASE_PATH
        self.residential_rates_data = ResidentialRatesData(self.db_path)
        self.test_rate = '1F'
        self.summer_start_month = 5
        self.start_year_month = '2024-01'

    def test_get_summer_charges(self):
        charges = self.residential_rates_data.get_summer_charges(
            self.test_rate, self.summer_start_month, self.start_year_month
        )
        self.assertIsNotNone(charges)
        self.assertIsInstance(charges, list)
        self.assertEqual(len(charges), 6)
        self.assertTrue(all(isinstance(charge, dict) for charge in charges))

    def test_get_winter_charges(self):
        charges = self.residential_rates_data.get_winter_charges(
            self.test_rate, self.summer_start_month, self.start_year_month
        )
        self.assertIsNotNone(charges)
        self.assertIsInstance(charges, list)
        self.assertEqual(len(charges), 6)
        self.assertTrue(all(isinstance(charge, dict)) for charge in charges)