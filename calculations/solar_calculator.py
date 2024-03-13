from models.pv_system import PVSystem
from models.rate import Rate
from calculations.environmental_impact_calculator import EnvironmentalImpactCalculator

class SolarSavingsCalculator:
    def __init__(self, rate, pv_system, current_monthly_consumption):
        self._rate = self._validate_rate(rate)
        self._pv_system = self._validate_pv_system(pv_system)
        self._current_monthly_consumption = current_monthly_consumption
        self._current_payment = rate.calculate_monthly_payments(current_monthly_consumption)
        self._offset = self._calculate_offset()
        self._invalidate_caches()

    def _validate_rate(self, value):
        if not isinstance(value, Rate):
            raise ValueError("The rate object must have an instance of Rate or its subclass")
        return value
    
    def _validate_pv_system(self, value):
        if not isinstance(value, PVSystem):
            raise ValueError("pv_system must be an instance of PVSystem")
        return value
    
    def _calculate_offset(self):
        if sum(self.current_monthly_consumption) == 0:
            return 1
        offset = sum(self._pv_system.monthly_energy_production) / sum(self._current_monthly_consumption)
        return offset
    
    def _invalidate_caches(self):
        self._new_monthly_consumption_cache = None
        self._new_lifetime_consumption_cache = None
        self._yearly_energy_savings_cache = None
        self._cumulative_energy_savings_cache = None
        self._new_monthly_payment_cache = None
        self._new_lifetime_payments_cache = None
        self._yearly_payments_savings_cache = None
        self._yearly_cashflow_cache = None
        self._cumulative_cashflow_cache = None

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = self._validate_rate(value)
        self._current_payment = self._rate.calculate_monthly_payments(self._current_monthly_consumption)
        self._invalidate_caches()

    @property
    def pv_system(self):
        return self._pv_system
    
    @pv_system.setter
    def pv_system(self, value):
        self._pv_system = self._validate_pv_system(value)
        self._offset =  self._calculate_offset()
        self._invalidate_caches()

    @property
    def current_monthly_consumption(self):
        return self._current_monthly_consumption
    
    @current_monthly_consumption.setter
    def current_monthly_consumption(self, value):
        self._current_monthly_consumption = value
        self._current_payment = self._rate.calculate_monthly_payments(self._current_monthly_consumption)
        self._offset = self._calculate_offset()
        self._invalidate_caches()

    @property
    def current_payment(self):
        return self._current_payment
    
    @property
    def offset(self):
        return self._offset
    
    def calculate_new_monthly_consumption(self):
        if self._new_monthly_consumption_cache is not None:
            return self._new_monthly_consumption_cache
        
        monthly_production = self._pv_system.monthly_energy_production
        new_monthly_consumption = []
        energy_bank = 0

        for current, production in zip(self.current_monthly_consumption, monthly_production):
            net_energy = production - current + energy_bank
            if net_energy >= 0:
                new_monthly_consumption.append(0)
                energy_bank = net_energy
            else:
                new_monthly_consumption.append(round(abs(net_energy), 2))
                energy_bank = 0
        
        if energy_bank > 0:
            for i in range(len(new_monthly_consumption)):
                if energy_bank <= 0:
                    break
                if new_monthly_consumption[i] > 0:
                    if new_monthly_consumption[i] <= energy_bank:
                        energy_bank -= new_monthly_consumption[i]
                        new_monthly_consumption[i] = 0
                    else:
                        new_monthly_consumption[i] -= energy_bank
                        new_monthly_consumption[i] = round(new_monthly_consumption[i], 2)
                        energy_bank = 0

        self._new_monthly_consumption_cache = new_monthly_consumption
        return new_monthly_consumption
    
    def calculate_monthly_energy_savings(self):
        new_monthly_consumption = self.calculate_new_monthly_consumption()
        monthly_energy_savings = [current - new for current, new in zip(self.current_monthly_consumption, new_monthly_consumption)]
        return monthly_energy_savings
    
    def calculate_new_lifetime_consumption(self):
        if self._new_lifetime_consumption_cache is not None:
            return self._new_lifetime_consumption_cache
        
        lifetime_production = self._pv_system.calculate_lifetime_production()
        annual_consumption = sum(self._current_monthly_consumption)
        new_lifetime_consumption = []
        
        if self._offset < 1:
            for production in lifetime_production:
                new_lifetime_consumption = [annual_consumption - production for production in lifetime_production]
        else:
            for production in lifetime_production:
                new_consumption = annual_consumption - production 
                new_lifetime_consumption.append(max(new_consumption, 0))

        self._new_lifetime_consumption_cache = new_lifetime_consumption
        return new_lifetime_consumption
    
    def calculate_yearly_energy_savings(self, cumulative=False):
        if self._yearly_energy_savings_cache is not None and not cumulative:
            return self._yearly_energy_savings_cache
        if self._cumulative_energy_savings_cache is not None and cumulative:
            return self._cumulative_cashflow_cache
        
        new_lifetime_consumption = self.calculate_new_lifetime_consumption()
        current_annual_consumption = sum(self.current_monthly_consumption)
        yearly_energy_savings = [current_annual_consumption - new_consumption for new_consumption in new_lifetime_consumption]

        if not cumulative:
            self._yearly_energy_savings_cache = yearly_energy_savings
            return yearly_energy_savings

        cumulative_energy_savings = [sum(yearly_energy_savings[:i+1]) for i in range(len(yearly_energy_savings))]
        self._cumulative_energy_savings_cache = cumulative_energy_savings
        return cumulative_energy_savings
    
    def calculate_new_monthly_payment(self):
        if self._new_monthly_payment_cache is not None:
            return self._new_monthly_payment_cache
        
        new_monthly_consumption = self.calculate_new_monthly_consumption()
        new_monthly_payment = self.rate.calculate_monthly_payments(new_monthly_consumption)
        
        self._calculate_new_monthly_payment = new_monthly_payment
        return new_monthly_payment
    
    def calculate_monthly_payment_savings(self):
        new_monthly_payment = self.calculate_new_monthly_payment()
        monthly_payment_savings = [current - new for current, new in zip(self._current_payment, new_monthly_payment)]
        return monthly_payment_savings
    
    def calculate_new_lifetime_payments(self, annual_inflation=0.05):
        if self._new_lifetime_payments_cache is not None:
            return self._new_lifetime_payments_cache
        
        new_monthly_consumption = self.calculate_new_monthly_consumption()
        year_1_consumption = sum(new_monthly_consumption)
        new_monthly_payment = self.calculate_new_monthly_payment()
        year_1_payment = round(sum(new_monthly_payment), 2)
        year_1_fix_charge_payment = self.rate.fix_charge
        annual_increase = 1 +  annual_inflation
        new_lifetime_payment = [year_1_payment]
        new_lifetime_consumption = self.calculate_new_lifetime_consumption()

        for i in range(1, len(new_lifetime_consumption)):
            if new_lifetime_consumption[i] == 0:
                annual_payment = year_1_fix_charge_payment * ( annual_increase ** i)
                new_lifetime_payment.append(round(annual_payment,2))
            else:
                annual_payment = (((year_1_payment - year_1_fix_charge_payment) * (new_lifetime_consumption[i] / year_1_consumption)) + year_1_fix_charge_payment) * (annual_increase ** i)
                new_lifetime_payment.append(round(annual_payment,2))
        
        self._new_lifetime_payments_cache = new_lifetime_payment
        return new_lifetime_payment
    
    def calculate_yearly_payments_savings(self, annual_inflation=0.05):
        if self._yearly_payments_savings_cache is not None:
            return self._yearly_payments_savings_cache
        
        new_lifetime_payments = self.calculate_new_lifetime_payments(annual_inflation)
        current_lifetime_payments = [round(sum(self._current_payment) * (1 + annual_inflation) ** i, 2) for i in range(len(new_lifetime_payments))]
        total_payments_savings = [current - new for current, new in zip(current_lifetime_payments, new_lifetime_payments)]
        
        self._yearly_payments_savings_cache = total_payments_savings
        return total_payments_savings
    
    def calculate_cash_flow(self, cumulative=False):
        if self._yearly_cashflow_cache is not None and not cumulative:
            return self._yearly_cashflow_cache
        if self._cumulative_cashflow_cache is not None and cumulative:
            return self._cumulative_cashflow_cache
        
        initial_outflow = -self._pv_system.installation_cost
        yearly_cash_flows = [initial_outflow]
        yearly_payments_savings = self.calculate_yearly_payments_savings()
        yearly_cash_flows.extend(yearly_payments_savings)

        if not cumulative:
            self._yearly_cashflow_cache = yearly_cash_flows
            return yearly_cash_flows
        
        cumulative_cash_flows = [sum(yearly_cash_flows[:i+1]) for i in range(len(yearly_cash_flows))]
        
        self._cumulative_cashflow_cache = cumulative_cash_flows
        return cumulative_cash_flows      

    def calculate_roi(self):
        cash_flows = self.calculate_cash_flow()
        total_investment = -cash_flows[0]
        total_returns = sum(cash_flows[1:])
        return round((total_returns - total_investment) /  total_investment, 2)
    
    def calculate_payback_period(self):
        cumulative_cash_flows = self.calculate_cash_flow(cumulative=True)
        first_positive_cashflow_year = -1
        last_negative_cashflow_year = -1
        for year, cash_flow in enumerate(cumulative_cash_flows):
            if cash_flow >= 0:
                first_positive_cashflow_year = year
                last_negative_cashflow_year = year - 1
                break
        
        if first_positive_cashflow_year == -1:
            return None
        
        last_negative_cashflow = cumulative_cash_flows[last_negative_cashflow_year]
        first_positive_cashflow = cumulative_cash_flows[first_positive_cashflow_year]
        fractional_year = -last_negative_cashflow / (first_positive_cashflow - last_negative_cashflow)
        payback_period = last_negative_cashflow_year + fractional_year

        return payback_period
    
    def calculate_environmental_impact(self):
        total_energy_savings = sum(self.calculate_yearly_energy_savings())
        calculator = EnvironmentalImpactCalculator(total_energy_savings)
        
        co2_saved = calculator.calculate_co2_emission_saved()
        trees_planted = calculator.calculate_trees_planted(co2_saved)

        return {
            "kg_co2_saved": co2_saved,
            "trees_planted": trees_planted
        }