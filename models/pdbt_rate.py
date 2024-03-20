from database.pdbt_rate_data import PdbtRateData 
from models.rate import Rate

class PdbtRate(Rate):
    def __init__(self, region_id, end_year_month, pdbt_rate_data=None):
        self._region_id = region_id
        super().__init__(end_year_month)
        self._pdbt_rate_data = pdbt_rate_data or PdbtRateData()
        self._charges = self._get_charges()

    def _get_charges(self):
        charges = self._pdbt_rate_data.get_charges(self._region_id, self._end_year_month)
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