import unittest
from calculations.environmental_impact_calculator import EnvironmentalImpactCalculator

class TestEnvironmentalImpactCalculator(unittest.TestCase):

    def test_energy_saved_kwh_positive(self):
        expected_energy_saved = 100
        calculator = EnvironmentalImpactCalculator(expected_energy_saved)
        actual_energy_saved = calculator._energy_saved_kwh
        self.assertEqual(actual_energy_saved, expected_energy_saved)

    def test_energy_saved_kwh_non_positive(self):
        energy_saved = -1
        with self.assertRaises(ValueError):
            EnvironmentalImpactCalculator(energy_saved)
    
    def test_calculate_co2_emission_saved(self):
        kg_co2_per_kwh = EnvironmentalImpactCalculator._KG_CO2_PER_KWH
        energy_saved = 100
        expected_co2_saved = round(energy_saved * kg_co2_per_kwh, 2)
        calculator = EnvironmentalImpactCalculator(energy_saved)
        actual_co2_saved = calculator.calculate_co2_emission_saved()
        self.assertEqual(expected_co2_saved, actual_co2_saved)

    def  test_calculate_trees_planted(self):
        energy_saved = 10000
        calculator = EnvironmentalImpactCalculator(energy_saved)
        co2_saved = calculator.calculate_co2_emission_saved()
        expected_trees_planted = co2_saved * EnvironmentalImpactCalculator._TREES_PLANTED_PER_KG_CO2
        actual_trees_planted = calculator.calculate_trees_planted()
        self.assertEqual(expected_trees_planted, actual_trees_planted)
