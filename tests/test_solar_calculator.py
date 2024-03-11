import unittest
from unittest.mock import Mock
from models.pv_system import PVSystem
from models.rate import Rate
from calculations.solar_calculator import SolarSavingsCalculator

class TestSolarSavingsCalculator(unittest.TestCase):
    def setUp(self):
        self.mock_pv_system = Mock(spec=PVSystem)
        self.mock_rate = Mock(spec=Rate)
        start = 100
        step = 10
        self.months = 12
        self.mock_rate.calculate_monthly_payments.return_value = [start + i * step for i in range(self.months)]
        self.mock_rate.fix_charge = 1860
        start = 120
        self.sample_consumption_data = [start + i * step for i in range(self.months)]
        self.mock_pv_system.monthly_energy_production = [100 for _ in range(self.months)]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, self.sample_consumption_data)

    def test_rate_validation(self):
        invalid_rate = Mock()
        with self.assertRaises(ValueError):
            SolarSavingsCalculator(invalid_rate, self.mock_pv_system, self.sample_consumption_data)
    
    def test_pv_system_validation(self):
        invalid_system_size = Mock()
        with self.assertRaises(ValueError):
            SolarSavingsCalculator(self.mock_rate, invalid_system_size, self.sample_consumption_data)

    def test_calculate_monthly_energy_savings(self):
        monthly_production_deficit = [100 for _ in range(self.months)]
        monthly_production_surplus = [170 for _ in range(self.months)]

        self.mock_pv_system.monthly_energy_production = monthly_production_deficit
        self.calculator.pv_system = self.mock_pv_system
        expected_monthly_energy_savings = monthly_production_deficit
        actual_monthly_energy_savings = self.calculator.calculate_monthly_energy_savings()
        self.assertEqual(actual_monthly_energy_savings, expected_monthly_energy_savings)

        self.mock_pv_system.monthly_energy_production = monthly_production_surplus
        self.calculator.pv_system = self.mock_pv_system
        expected_monthly_energy_savings = [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 170]
        actual_monthly_energy_savings = self.calculator.calculate_monthly_energy_savings()
        self.assertEqual(actual_monthly_energy_savings, expected_monthly_energy_savings)

    def test_calculate_total_energy_savings(self):
        step = 50
        lifetime = 10
        
        monthly_production_deficit = [150 for _ in range(self.months)]
        start = sum(monthly_production_deficit)
        lifetime_production_deficit = [start - i * step for i in range(lifetime)]

        monthly_production_surplus = [200 for _ in range(self.months)]
        start = sum(monthly_production_surplus)
        lifetime_production_surplus = [start - i * step for i in range(lifetime)]

        self.mock_pv_system.monthly_energy_production = monthly_production_deficit
        self.mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_deficit
        self.calculator.pv_system = self.mock_pv_system
        expected_total_savings = lifetime_production_deficit
        actual_total_savings = self.calculator.calculate_total_energy_savings()
        self.assertEqual(actual_total_savings, expected_total_savings)

        self.mock_pv_system.monthly_energy_production = monthly_production_surplus
        self.mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_surplus
        self.calculator.pv_system = self.mock_pv_system
        expected_total_savings = [min(production, sum(self.sample_consumption_data)) for production in lifetime_production_surplus]
        actual_total_savings = self.calculator.calculate_total_energy_savings()
        self.assertEqual(actual_total_savings, expected_total_savings)

    def test_calculate_new_lifetime_consumption(self):
        step = 50
        lifetime = 10

        annual_energy_production_deficit = [150 for _ in range(self.months)]
        start = sum(annual_energy_production_deficit)
        lifetime_production_deficit = [start - i * step for i in range(lifetime)]
        
        annual_energy_production_surplus = [200 for _ in range(self.months)]
        start = sum(annual_energy_production_surplus)
        lifetime_production_surplus= [start - i * step for i in range(lifetime)]

        self.mock_pv_system.monthly_energy_production = annual_energy_production_deficit
        self.mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_deficit
        self.calculator.pv_system = self.mock_pv_system
        expected_consumption_deficit = [sum(self.sample_consumption_data) - production for production in lifetime_production_deficit]
        actual_consumption_deficit = self.calculator.calculate_new_lifetime_consumption()
        self.assertEqual(actual_consumption_deficit, expected_consumption_deficit)

        self.mock_pv_system.monthly_energy_production = annual_energy_production_surplus
        self.mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_surplus
        self.calculator.pv_system = self.mock_pv_system
        expected_consumption_surplus = [max(sum(self.sample_consumption_data) - production, 0) for production in lifetime_production_surplus]
        actual_consumption_surplus = self.calculator.calculate_new_lifetime_consumption()
        self.assertEqual(actual_consumption_surplus, expected_consumption_surplus)

    def test_calculate_new_monthly_payment(self):
        self.mock_rate.calculate_monthly_payments.return_value = [90 + i * 5 for i in range(self.months)]
        self.mock_pv_system.monthly_energy_production = [95 + i * 2 for i in range(self.months)]
        self.calculator.rate = self.mock_rate
        self.calculator.pv_system = self.mock_pv_system
        expected_new_monthly_payments = self.mock_rate.calculate_monthly_payments(self.calculator.calculate_new_monthly_consumption())
        actual_new_monthly_payments = self.calculator.calculate_new_monthly_payment()
        self.assertEqual(actual_new_monthly_payments, expected_new_monthly_payments)

    def test_calculate_monthly_payment_savings(self):
        initial_payments = [100 + i * 5 for i in range(self.months)]
        new_payments = [95 + i * 4 for i in range(self.months)]
        self.mock_rate.calculate_monthly_payments.side_effect = [initial_payments, new_payments]
        self.calculator.rate = self.mock_rate
        self.calculator.pv_system = self.mock_pv_system
        expected_monthly_payment_savings = [i - j for i, j in zip(initial_payments, new_payments)]
        actual_monthly_payment_savings = self.calculator.calculate_monthly_payment_savings()
        self.assertEqual(actual_monthly_payment_savings, expected_monthly_payment_savings)

    def test_calculate_new_lifetime_payments(self):
        lifetime = 25
        annual_increase = 1.05
        surplus_consumption = [0 for _ in range(self.months)]
        surplus_lifetime_consumption = [0 for _ in range(lifetime)]
        self.mock_pv_system.calculate_lifetime_production.return_value = surplus_lifetime_consumption
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, surplus_consumption)
        expected_lifetime_payments_surplus = [round(self.mock_rate.fix_charge * ((annual_increase) ** i), 2) for i in range(lifetime)]
        actual_lifetime_payments_surplus = self.calculator.calculate_new_lifetime_payments()
        self.assertEqual(actual_lifetime_payments_surplus, expected_lifetime_payments_surplus)

        deficit_consumption = self.sample_consumption_data
        deficit_lifetime_consumption = [sum(deficit_consumption) - i * 1000 for i in range(lifetime)]
        self.mock_pv_system.calculate_lifetime_production.return_value = deficit_lifetime_consumption
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, deficit_consumption)
        year_1_payment = round(sum(self.mock_rate.calculate_monthly_payments(deficit_consumption)), 2)
        year_1_consumption = sum(deficit_consumption)
        expected_lifetime_payments_deficit = [year_1_payment]
        for i in range(1, lifetime):
            annual_payment = (((year_1_payment - self.mock_rate.fix_charge) * (deficit_lifetime_consumption[i] / year_1_consumption)) + self.mock_rate.fix_charge) * (1.05 ** i)
            expected_lifetime_payments_deficit.append(round(annual_payment, 2))
        actual_lifetime_payments_deficit = self.calculator.calculate_new_lifetime_payments()
        self.assertEqual(actual_lifetime_payments_deficit, expected_lifetime_payments_deficit)

    def test_calculate_total_payment_savings(self):
        lifetime = 25
        annual_increase = 1.05

        surplus_consumption = [0 for _ in range(self.months)]        
        self.mock_pv_system.calculate_lifetime_production.return_value = [99999 for _ in range(lifetime)]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, surplus_consumption)
        year_1_payment = sum(self.mock_rate.calculate_monthly_payments(surplus_consumption))
        current_lifetime_payment = [year_1_payment * ((annual_increase) ** i) for i in range(lifetime)]
        new_lifetime_payments = [self.mock_rate.fix_charge * ((annual_increase) ** i) for i in range(lifetime)]
        expected_payments_savings = [round(current - new, 2) for current, new in zip(current_lifetime_payment, new_lifetime_payments)]
        actual_payments_savings = self.calculator.calculate_total_payment_savings()
        self.assertEqual(actual_payments_savings, expected_payments_savings)

        deficit_consumption = self.sample_consumption_data
        self.mock_pv_system.calculate_lifetime_production.return_value = [50 for _ in range(lifetime)]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, deficit_consumption)
        year_1_payment = round(sum(self.mock_rate.calculate_monthly_payments(deficit_consumption)), 2)
        new_lifetime_payments = self.calculator.calculate_new_lifetime_payments()
        current_lifetime_payment = [year_1_payment * (annual_increase ** i) for i in range(lifetime)]
        expected_payments_savings = [round(current - new, 2) for current, new in zip(current_lifetime_payment, new_lifetime_payments)]
        actual_payments_savings = self.calculator.calculate_total_payment_savings()
        self.assertEqual(actual_payments_savings, expected_payments_savings)

if __name__ == '__main__':
    unittest.main()
