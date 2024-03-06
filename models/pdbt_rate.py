from database.pdbt_rate_data import PdbtRateData 
from utils.date_utils import calculate_start_month

class PdbtRate:
    IVA_RATE = 1.08

    def __init__(self, state, end_month, pdbt_rate_data=None):
        self._pdbt_rate_data = pdbt_rate_data or PdbtRateData()
        self._charges = self._pdbt_rate_data.get_charges(state, calculate_start_month(end_month), end_month)
    
    def calculate_monthly_payments(self, monthly_consumption):
        if not self._charges or len(self._charges) != 12:
            raise ValueError("Rates data is incomplete or not available. Please fetch correct rates before calculating payments.")
        
        if len(monthly_consumption) != 12:
            raise ValueError("Monthly consumptions list must contain 12 items, one for each month.")

        return [self._calculate_payment(rate, consumption) for rate, consumption in zip(self._charges, monthly_consumption)]
        
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