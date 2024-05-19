from database.commercial_rates_data import CommercialRatesData
from models.rate import Rate

class GdmtoRate(Rate):
    LOAD_FACTOR = 0.55
    LOW_VOLTAGE_RATE = 0.02
    DAP_CHARGE = 15

    def __init__(self, location, end_year_month, gdmto_rate_data=None):
        super().__init__(location, end_year_month, needs_days_in_month=True)
        self._gdmto_rate_data = gdmto_rate_data or CommercialRatesData("GDMTO")
        self._charges = self._get_charges()
    
    def _get_charges(self):
        charges = self._gdmto_rate_data.get_charges(self._location.region_id, self._end_year_month)
        charges = self._validate_charges(charges)
        return charges
    
    def _validate_demand(self, demand):
        if not isinstance(demand, int) or demand < 0:
            raise ValueError("Demand must be a positive integer")
        return demand
    
    def _validate_power_factor(self, power_factor):
        if not isinstance(power_factor, (int, float)) or not (30 <= power_factor <= 100):
            raise ValueError("Power factor must be a number between 30 and 100")
        return power_factor
    
    def _calculate_payment(self, charge, consumption, days_in_month, demand, power_factor):
        power_factor = self._validate_power_factor(power_factor)
        demand = self._validate_demand(demand)
        capacity_demand = self._calculate_demand(consumption, days_in_month)
        distribution_demand = min(demand, capacity_demand)
        power_factor_rate = self._calculate_power_factor_rate(power_factor)
    
        cost_components = [
            charge["supplier"],
            consumption * charge["transmission"],
            consumption * charge["cenace"],
            consumption * charge["services"],
            consumption * charge["energy"],
            capacity_demand * charge["capacity"],
            distribution_demand * charge["distribution"],
        ]
        
        subtotal = sum(cost_components) * (1 + self.LOW_VOLTAGE_RATE)
        power_factor_charge = subtotal * power_factor_rate
        total_before_iva = subtotal + power_factor_charge
        total_cost = (total_before_iva * self.IVA_RATE) + self.DAP_CHARGE
        return round(total_cost, 2)
    
    def _calculate_demand(self, consumption, days_in_month):
        demand = consumption / (24 * days_in_month * self.LOAD_FACTOR)
        return round(demand, 2)
    
    def _calculate_power_factor_rate(self, power_factor):
        if power_factor == 90:
            return 0
        if power_factor > 90:
            power_factor_charge = - 0.25 * (1 - (90 / power_factor))
            return power_factor_charge
        if power_factor < 90:
            power_factor_charge = 0.6 * ((90 / power_factor) - 1)
            return power_factor_charge