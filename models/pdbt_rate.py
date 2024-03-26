from database.commercial_rates_data import CommercialRatesData
from models.rate import Rate

class PdbtRate(Rate):
    def __init__(self, location, end_year_month, pdbt_rate_data=None):
        super().__init__(location, end_year_month)
        self._pdbt_rate_data = pdbt_rate_data or CommercialRatesData('PDBT')
        self._charges = self._get_charges()

    def _get_charges(self):
        charges = self._pdbt_rate_data.get_charges(self._location.region_id, self._end_year_month)
        charges = self._validate_charges(charges)
        return charges
    
    def _calculate_payment(self, charge, consumption):
        # Supplier charge is the only concept charged when there is no consumption, being this the fix charge
        if consumption == 0:
            return charge["supplier"] * self.IVA_RATE
        
        cost_components = [
            consumption * charge["transmission"],
            consumption * charge["distribution"],
            consumption * charge["cenace"],
            charge["supplier"],
            consumption * charge["services"],
            consumption * charge["energy"],
            consumption * charge["capacity"],
        ]
        total_cost = sum(cost_components) * self.IVA_RATE
        return round(total_cost, 2)