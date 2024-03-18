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
        start = 120
        self.sample_consumption_data = [start + i * step for i in range(self.months)]
        self.mock_pv_system.calculate_monthly_energy_production.return_value = [100 for _ in range(self.months)]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, self.sample_consumption_data)

    def test_rate_validation(self):
        invalid_rate = Mock()
        with self.assertRaises(ValueError):
            SolarSavingsCalculator(invalid_rate, self.mock_pv_system, self.sample_consumption_data)
    
    def test_pv_system_validation(self):
        invalid_system_size = Mock()
        with self.assertRaises(ValueError):
            SolarSavingsCalculator(self.mock_rate, invalid_system_size, self.sample_consumption_data)

    def test_calculate_offset(self):
        energy_production = [100 for _ in range(self.months)]
        self.mock_pv_system.calculate_monthly_energy_production.return_value = energy_production
        expected_offset = round(sum(energy_production) / sum(self.sample_consumption_data), 2)
        actual_offset = self.calculator.calculate_offset()
        self.assertEqual(actual_offset, expected_offset)

    def test_calculate_monthly_energy_savings(self):
        monthly_production_deficit = [100 for _ in range(self.months)]
        monthly_production_surplus = [170 for _ in range(self.months)]

        self.mock_pv_system.calculate_monthly_energy_production.return_value = monthly_production_deficit
        self.calculator.pv_system = self.mock_pv_system
        expected_monthly_energy_savings = monthly_production_deficit
        actual_monthly_energy_savings = self.calculator.calculate_monthly_energy_savings()
        self.assertEqual(actual_monthly_energy_savings, expected_monthly_energy_savings)

        self.mock_pv_system.calculate_monthly_energy_production.return_value = monthly_production_surplus
        self.calculator.pv_system = self.mock_pv_system
        expected_monthly_energy_savings = [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 170]
        actual_monthly_energy_savings = self.calculator.calculate_monthly_energy_savings()
        self.assertEqual(actual_monthly_energy_savings, expected_monthly_energy_savings)

    def test_calculate_new_lifetime_consumption(self):
        step = 50
        lifetime = 10

        annual_energy_production_deficit = [150 for _ in range(self.months)]
        start = sum(annual_energy_production_deficit)
        lifetime_production_deficit = [start - i * step for i in range(lifetime)]
        
        annual_energy_production_surplus = [200 for _ in range(self.months)]
        start = sum(annual_energy_production_surplus)
        lifetime_production_surplus= [start - i * step for i in range(lifetime)]

        self.mock_pv_system.calculate_monthly_energy_production.return_value = annual_energy_production_deficit
        self.mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_deficit
        self.calculator.pv_system = self.mock_pv_system
        expected_consumption_deficit = [sum(self.sample_consumption_data) - production for production in lifetime_production_deficit]
        actual_consumption_deficit = self.calculator.calculate_new_lifetime_consumption()
        self.assertEqual(actual_consumption_deficit, expected_consumption_deficit)

        self.mock_pv_system.calculate_monthly_energy_production.return_value = annual_energy_production_surplus
        self.mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_surplus
        self.calculator.pv_system = self.mock_pv_system
        expected_consumption_surplus = [max(sum(self.sample_consumption_data) - production, 0) for production in lifetime_production_surplus]
        actual_consumption_surplus = self.calculator.calculate_new_lifetime_consumption()
        self.assertEqual(actual_consumption_surplus, expected_consumption_surplus)

    def test_calculate_yearly_energy_savings(self):
        step = 50
        lifetime = 10
        
        monthly_production_deficit = [150 for _ in range(self.months)]
        start = sum(monthly_production_deficit)
        lifetime_production_deficit = [start - i * step for i in range(lifetime)]

        self.mock_pv_system.calculate_monthly_energy_production.return_value = monthly_production_deficit
        self.mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_deficit
        self.calculator.pv_system = self.mock_pv_system
        
        expected_total_savings = lifetime_production_deficit
        actual_total_savings = self.calculator.calculate_yearly_energy_savings()
        self.assertEqual(actual_total_savings, expected_total_savings)

        expected_cumulative_savings = [sum(expected_total_savings[:i + 1]) for i in range(len(expected_total_savings))]
        actual_cumulative_savings = self.calculator.calculate_yearly_energy_savings(cumulative=True)
        self.assertEqual(actual_cumulative_savings, expected_cumulative_savings)
        
        monthly_production_surplus = [200 for _ in range(self.months)]
        start = sum(monthly_production_surplus)
        lifetime_production_surplus = [start - i * step for i in range(lifetime)]

        self.mock_pv_system.calculate_monthly_energy_production.return_value = monthly_production_surplus
        self.mock_pv_system.calculate_lifetime_production.return_value = lifetime_production_surplus
        self.calculator.pv_system = self.mock_pv_system
        
        expected_total_savings = [min(production, sum(self.sample_consumption_data)) for production in lifetime_production_surplus]
        actual_total_savings = self.calculator.calculate_yearly_energy_savings()
        self.assertEqual(actual_total_savings, expected_total_savings)

        expected_cumulative_savings_surplus = [sum(expected_total_savings[:i + 1]) for i in range(len(expected_total_savings))]
        actual_cumulative_savings_surplus = self.calculator.calculate_yearly_energy_savings(cumulative=True)
        self.assertEqual(actual_cumulative_savings_surplus, expected_cumulative_savings_surplus)

    def test_calculate_current_monthly_payment(self):
        self.mock_rate.calculate_monthly_payments.return_value = [120 + i * 5 for i in range(self.months)]
        self.mock_pv_system.calculate_monthly_energy_production.return_value = [0 for _ in range(self.months)]
        self.calculator.rate = self.mock_rate
        self.calculator.pv_system = self.mock_pv_system
        expected_current_monthly_payments = self.mock_rate.calculate_monthly_payments(self.sample_consumption_data)
        actual_current_monthly_payments = self.calculator.calculate_current_monthly_payment()
        self.assertEqual(actual_current_monthly_payments, expected_current_monthly_payments)
    
    def test_calculate_new_monthly_payment(self):
        self.mock_rate.calculate_monthly_payments.return_value = [90 + i * 5 for i in range(self.months)]
        self.mock_pv_system.calculate_monthly_energy_production.return_value = [95 + i * 2 for i in range(self.months)]
        self.calculator.rate = self.mock_rate
        self.calculator.pv_system = self.mock_pv_system
        expected_new_monthly_payments = self.mock_rate.calculate_monthly_payments(self.calculator.calculate_new_monthly_consumption())
        actual_new_monthly_payments = self.calculator.calculate_new_monthly_payment()
        self.assertEqual(actual_new_monthly_payments, expected_new_monthly_payments)

    def test_calculate_monthly_payment_savings(self):
        initial_payments = [100 + i * 5 for i in range(self.months)]
        new_payments = [95 + i * 4 for i in range(self.months)]
        self.mock_rate.calculate_monthly_payments.side_effect = [new_payments, initial_payments]
        self.calculator.rate = self.mock_rate
        self.calculator.pv_system = self.mock_pv_system
        expected_monthly_payment_savings = [i - j for i, j in zip(initial_payments, new_payments)]
        actual_monthly_payment_savings = self.calculator.calculate_monthly_payment_savings()
        self.assertEqual(actual_monthly_payment_savings, expected_monthly_payment_savings)

    def test_calculate_new_lifetime_payments(self):
        lifetime = 25
        annual_increase = 1.05
        fix_charge_payment = 1860

        surplus_consumption = [0 for _ in range(self.months)]
        surplus_lifetime_consumption = [0 for _ in range(lifetime)]
        self.mock_pv_system.calculate_lifetime_production.return_value = surplus_lifetime_consumption
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, surplus_consumption)
        expected_lifetime_payments_surplus = [round(fix_charge_payment * ((annual_increase) ** i), 2) for i in range(lifetime)]
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
            annual_payment = (((year_1_payment - fix_charge_payment) * (deficit_lifetime_consumption[i] / year_1_consumption)) + fix_charge_payment) * (1.05 ** i)
            expected_lifetime_payments_deficit.append(round(annual_payment, 2))
        actual_lifetime_payments_deficit = self.calculator.calculate_new_lifetime_payments()
        self.assertEqual(actual_lifetime_payments_deficit, expected_lifetime_payments_deficit)

    def test_calculate_yearly_payments_savings(self):
        lifetime = 25
        annual_increase = 1.05
        fix_charge_payment = 1860
        surplus_consumption = [0 for _ in range(self.months)]        
        self.mock_pv_system.calculate_lifetime_production.return_value = [99999 for _ in range(lifetime)]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, surplus_consumption)
        year_1_payment = sum(self.mock_rate.calculate_monthly_payments(surplus_consumption))
        current_lifetime_payment = [year_1_payment * ((annual_increase) ** i) for i in range(lifetime)]
        new_lifetime_payments = [fix_charge_payment * ((annual_increase) ** i) for i in range(lifetime)]
        expected_payments_savings = [round(current - new, 2) for current, new in zip(current_lifetime_payment, new_lifetime_payments)]
        actual_payments_savings = self.calculator.calculate_yearly_payments_savings()
        self.assertEqual(actual_payments_savings, expected_payments_savings)

        deficit_consumption = self.sample_consumption_data
        self.mock_pv_system.calculate_lifetime_production.return_value = [50 for _ in range(lifetime)]
        self.calculator = SolarSavingsCalculator(self.mock_rate, self.mock_pv_system, deficit_consumption)
        year_1_payment = round(sum(self.mock_rate.calculate_monthly_payments(deficit_consumption)), 2)
        new_lifetime_payments = self.calculator.calculate_new_lifetime_payments()
        current_lifetime_payment = [year_1_payment * (annual_increase ** i) for i in range(lifetime)]
        expected_payments_savings = [round(current - new, 2) for current, new in zip(current_lifetime_payment, new_lifetime_payments)]
        actual_payments_savings = self.calculator.calculate_yearly_payments_savings()
        self.assertEqual(actual_payments_savings, expected_payments_savings)
    
    def test_calculate_cash_flow(self):
        lifetime = 10
        step = 50
        installation_cost = 10000
        self.mock_pv_system.calculate_installation_cost.return_value = installation_cost
        yearly_payments_savings = [step * i for i in range(1, lifetime + 1)]
        self.calculator.calculate_yearly_payments_savings = Mock(return_value=yearly_payments_savings )

        expected_yearly_cash_flows = [-installation_cost] + yearly_payments_savings
        actual_yearly_cash_flows = self.calculator.calculate_cash_flow()
        self.assertEqual(actual_yearly_cash_flows, expected_yearly_cash_flows)

        expected_cumulative_cash_flows = [sum(expected_yearly_cash_flows[:i+1]) for i in range(len(expected_yearly_cash_flows))]
        actual_cumulative_cash_flows = self.calculator.calculate_cash_flow(cumulative=True)
        self.assertEqual(actual_cumulative_cash_flows, expected_cumulative_cash_flows)

    def test_calculate_roi(self):
        initial_investment_profitable = -1000
        yearly_returns_profitable = [300, 400, 350, 450]
        self.calculator.calculate_cash_flow = Mock(return_value=[initial_investment_profitable] + yearly_returns_profitable)

        expected_roi_profitable = round((sum(yearly_returns_profitable) - abs(initial_investment_profitable)) / abs(initial_investment_profitable), 2)
        actual_roi_profitable = self.calculator.calculate_roi()
        self.assertEqual(actual_roi_profitable, expected_roi_profitable)

        initial_investment_non_profitable = -2000
        yearly_returns_non_profitable = yearly_returns_profitable  
        self.calculator.calculate_cash_flow = Mock(return_value=[initial_investment_non_profitable] + yearly_returns_non_profitable)

        expected_roi_non_profitable = round((sum(yearly_returns_non_profitable) - abs(initial_investment_non_profitable)) / abs(initial_investment_non_profitable), 2)
        actual_roi_non_profitable = self.calculator.calculate_roi()
        self.assertEqual(actual_roi_non_profitable, expected_roi_non_profitable)

    def test_calculate_payback_period(self):
        initial_investment_profitable = -1000
        cumulative_returns_profitable = [-700, -300, 100, 600]
        self.calculator.calculate_cash_flow = Mock(cumulative=True, return_value=[initial_investment_profitable] + cumulative_returns_profitable)
        
        last_negative_cashflow_profitable = cumulative_returns_profitable[-3]
        first_positive_cashflow_profitable = cumulative_returns_profitable[-2]
        fractional_year_profitable = -last_negative_cashflow_profitable / (first_positive_cashflow_profitable - last_negative_cashflow_profitable)
        expected_payback_period_profitable = 2 + fractional_year_profitable

        actual_payback_period_profitable = self.calculator.calculate_payback_period()
        self.assertEqual(actual_payback_period_profitable, expected_payback_period_profitable)

        initial_investment_non_profitable = -20000
        cumulative_returns_non_profitable = [-19900, -19800, -19700, -19500]
        self.calculator.calculate_cash_flow = Mock(cumulative=True, return_value=[initial_investment_non_profitable] + cumulative_returns_non_profitable)
        
        expected_payback_period_non_profitable = None
        actual_payback_period_non_profitable = self.calculator.calculate_payback_period()
        self.assertEqual(actual_payback_period_non_profitable, expected_payback_period_non_profitable)

    def test_calculate_environmental_impact(self):
        lifetime = 25
        annual_savings = 1000
        kg_co2_per_kwh = 0.458
        trees_planted_per_kg_co2 = 0.001
        yearly_energy_savings = [annual_savings for _ in range(lifetime)]
        self.calculator.calculate_yearly_energy_savings = Mock(return_value=yearly_energy_savings)
        environmental_impact = self.calculator.calculate_environmental_impact()

        expected_co2_saved =  round(sum(yearly_energy_savings) * kg_co2_per_kwh, 2)
        actual_co2_saved = environmental_impact["kg_co2_saved"]
        self.assertEqual(actual_co2_saved, expected_co2_saved)

        expected_trees_planted = round(expected_co2_saved * trees_planted_per_kg_co2, 2)
        actual_trees_planted = environmental_impact["trees_planted"]
        self.assertEqual(actual_trees_planted, expected_trees_planted)
        
if __name__ == '__main__':
    unittest.main()