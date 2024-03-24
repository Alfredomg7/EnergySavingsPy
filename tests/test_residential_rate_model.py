import unittest
from unittest.mock import Mock
from database.residential_rates_data import ResidentialRatesData
from models.residential_rate import ResidentialRate
from models.location import Location

class TestResidentialRateYearly(unittest.TestCase):

    def setUp(self):
        self.location = Mock(spec=Location)
        self.location.residential_rate = '1F'
        self.location.summer_start_month = 5
        self.end_year_month = '2024-12'
        self.residential_rates_data = Mock(spec=ResidentialRatesData)
        self.mock_charges = [
            {'billing_period': f'2024-{month:02}', 'basic': 0.05, 'low_intermediate': 0.1, 'intermediate':0.2,
             'high_intermediate': 0.3, 'excess': 0.4} for month in range(1, 13)
        ]
        self.residential_rates_data.get_charges.return_value = self.mock_charges

    def test_calculate_payment_yearly(self):
        residential_rate = ResidentialRate(self.location, self.end_year_month, self.residential_rates_data)
        monthly_consumptions = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
        expected_payments = [21.6, 43.2, 129.6, 172.8, 54, 64.8, 75.6, 86.4, 97.2, 108, 475.2, 518.4]
        
        for i, consumption in enumerate(monthly_consumptions):
            payment = residential_rate._calculate_payment(self.mock_charges[i], consumption)
            self.assertAlmostEqual(payment, expected_payments[i])

if __name__ == '__main__':
    unittest.main()
