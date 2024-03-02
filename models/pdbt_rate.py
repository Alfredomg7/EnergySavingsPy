from database.pdbt_rate_data import PdbtRateData 
from utils.date_utils import calculate_start_month

class PdbtRate:
    IVA_RATE = 1.08

    def __init__(self, state, end_month, pdbt_rate_data=None):
        self.pdbt_rate_data = pdbt_rate_data or PdbtRateData()
        self.rates = self.pdbt_rate_data.get_charges(state, calculate_start_month(end_month), end_month)
    
    def calculate_monthly_payments(self, monthly_consumption):
        if not self.rates or len(self.rates) != 12:
            raise ValueError("Rates data is incomplete or not available. Please fetch correct rates before calculating payments.")
        
        if len(monthly_consumption) != 12:
            raise ValueError("Monthly consumptions list must contain 12 items, one for each month.")

        monthly_payments = []
        for rate, consumption in zip(self.rates, monthly_consumption):
            monthly_cost = sum([
                consumption * rate['transmission'],
                consumption * rate['distribution'],
                consumption * rate['cenace'],
                rate['supplier'],
                consumption * rate['services'],
                consumption * rate ['energy'],
                consumption * rate ['capacity']
            ])

            monthly_cost *= self.IVA_RATE
            monthly_payments.append(monthly_cost)
        
        return monthly_payments