from database.pdbt_rate_data import PdbtRateData 
from utils.date_utils import calculate_start_month
from models.rate import Rate

class PdbtRate(Rate):
    def __init__(self, state, end_month, pdbt_rate_data=None):
        super().__init__(state, end_month)
        self._pdbt_rate_data = pdbt_rate_data or PdbtRateData()
        self._charges = self._pdbt_rate_data.get_charges(self._state, calculate_start_month(self._end_month), self._end_month)
        self._fix_charge = self._calculate_fix_charge()

    def _calculate_fix_charge(self):
        self._validate_charges()
        return sum(self._charges[i]["supplier"] for i in range(12)) * self.IVA_RATE
    
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