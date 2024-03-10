from models.pv_system import PVSystem
from models.rate import Rate

class SolarSavingsCalculator:
    def __init__(self, rate, pv_system, current_monthly_consumption):
        self._rate = self._validate_rate(rate)
        self._pv_system = self._validate_pv_system(pv_system)
        self._current_monthly_consumption = current_monthly_consumption
        self._current_payment = rate.calculate_monthly_payments(current_monthly_consumption)
        self._offset = self._calculate_offset()

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
        offset = sum(self._pv_system.calculate_annual_energy_production()) / sum(self._current_monthly_consumption)
        return offset
    
    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = self._validate_rate(value)
        self._current_payment = self._rate.calculate_monthly_payments(self._current_monthly_consumption)

    @property
    def pv_system(self):
        return self._pv_system
    
    @pv_system.setter
    def pv_system(self, value):
        self._pv_system = self._validate_pv_system(value)
        self._offset =  self._calculate_offset()

    @property
    def current_monthly_consumption(self):
        return self._current_monthly_consumption
    
    @current_monthly_consumption.setter
    def current_monthly_consumption(self, value):
        self._current_monthly_consumption = value
        self._current_payment = self._rate.calculate_monthly_payments(self._current_monthly_consumption)
        self._offset = self._calculate_offset()

    @property
    def current_payment(self):
        return self._current_payment
    
    @property
    def offset(self):
        return self._offset
    
    def calculate_new_monthly_consumption(self):
        monthly_production = self._pv_system.calculate_annual_energy_production()
        new_monthly_consumption = []
        energy_bank = 0

        for current, production in zip(self.current_monthly_consumption, monthly_production):
            net_energy = production - current + energy_bank
            if net_energy >= 0:
                new_monthly_consumption.append(0)
                energy_bank = net_energy
            else:
                net_deficit = net_energy + energy_bank
                if net_deficit >= 0:
                    energy_bank = net_deficit
                    new_monthly_consumption.append(0)
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

        return new_monthly_consumption
    
    def calculate_monthly_energy_savings(self):
        new_monthly_consumption = self.calculate_new_monthly_consumption()
        monthly_energy_savings = [current - new for current, new in zip(self.current_monthly_consumption, new_monthly_consumption)]
        return monthly_energy_savings
    
    def calculate_new_lifetime_consumption(self):
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

        return new_lifetime_consumption
    
    def calculate_total_energy_savings(self):
        new_lifetime_consumption = self.calculate_new_lifetime_consumption()
        current_annual_consumption = sum(self.current_monthly_consumption)
        total_energy_savings = [current_annual_consumption - new_consumption for new_consumption in new_lifetime_consumption]
        return total_energy_savings

    def calculate_new_monthly_payment(self):
        return self.rate.calculate_monthly_payments(self.calculate_new_monthly_consumption())
    
    def calculate_monthly_payment_savings(self):
        new_monthly_payment = self.calculate_new_monthly_payment()
        monthly_payment_savings = [current - new for current, new in zip(self._current_payment, new_monthly_payment)]
        return monthly_payment_savings
    
    def calculate_new_lifetime_payments(self, annual_inflation=0.05):
        new_lifetime_consumption = self.calculate_new_lifetime_consumption()
        year_1_payment = round(sum(self.calculate_new_monthly_payment()), 2)
        year_1_consumption = sum(self.calculate_new_monthly_consumption())
        year_1_fix_charge_payment = self.rate.fix_charge
        annual_increase = 1 +  annual_inflation
        new_lifetime_payment = [year_1_payment]

        for i in range(1, len(new_lifetime_consumption)):
            if new_lifetime_consumption[i] == 0:
                annual_payment = year_1_fix_charge_payment * ( annual_increase ** i)
                new_lifetime_payment.append(round(annual_payment,2))
            else:
                annual_payment = (((year_1_payment - year_1_fix_charge_payment) * (new_lifetime_consumption[i] / year_1_consumption)) + year_1_fix_charge_payment) * (annual_increase ** i)
                new_lifetime_payment.append(round(annual_payment,2))
        
        return new_lifetime_payment
    
    def calculate_total_payment_savings(self, annual_inflation=0.05):
        new_lifetime_payments = self.calculate_new_lifetime_payments(annual_inflation)
        current_lifetime_payments = [round(sum(self._current_payment) * (1 + annual_inflation) ** i, 2) for i in range(len(new_lifetime_payments))]
        total_payments_savings = [current - new for current, new in zip(current_lifetime_payments, new_lifetime_payments)]
        return total_payments_savings
