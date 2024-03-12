class EnvironmentalImpactCalculator:
    _KG_CO2_PER_KWH = 0.458
    _TREES_PLANTED_PER_KG_CO2 = 0.001

    def __init__(self, energy_saved_kwh, kg_co2_per_kwh=0.458, trees_planted_per_kg_co2 = 0.001):
        self._energy_saved_kwh = self._validate_energy_saved_kwh(energy_saved_kwh)
        
    def _validate_energy_saved_kwh(self, value):
        if not value >= 0:
            raise ValueError("energy_saved_kwh must be a non-negative value")
        return value
    
    @property
    def energy_saved_kwh(self):
        return self._energy_saved_kwh
    
    energy_saved_kwh.setter
    def energy_saved_kwh(self, value):
        self._energy_saved_kwh = self._validate_energy_saved_kwh(value)

    def calculate_co2_emission_saved(self):
        co2_emissions_saved = round(self._energy_saved_kwh * self._KG_CO2_PER_KWH, 2)
        return co2_emissions_saved
    
    def calculate_trees_planted(self, co2_emissions_saved=None):
        if co2_emissions_saved is None:
            co2_emissions_saved = self.calculate_co2_emission_saved()
        
        trees_planted = round(co2_emissions_saved *  self._TREES_PLANTED_PER_KG_CO2, 2)

        return trees_planted
    