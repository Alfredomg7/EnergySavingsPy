from database.pdbt_rate_data import PdbtRateData 
from models.rate import Rate

class PdbtRate(Rate):
    def __init__(self, region_id, end_month, pdbt_rate_data=None):
        super().__init__(region_id, end_month)
        self._pdbt_rate_data = pdbt_rate_data or PdbtRateData()
        self._charges = self._get_charges()

    def _get_charges(self):
        charges = self._pdbt_rate_data.get_charges(self._region_id, self._end_month)
        charges = self._validate_charges(charges)
        return charges
    
    def _calculate_payment(self, charge, consumption):    
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