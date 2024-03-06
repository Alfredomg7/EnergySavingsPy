from models.pv_system import PVSystem

class SolarSavingsCalculator:
    def __init__(self, rate, current_monthly_consumption):
        self._rate = self._validate_rate(rate)
        self._current_monthly_consumption = self._validate_current_monthly_consumption(current_monthly_consumption)
        self._current_payment = rate.calculate_monthly_payments(current_monthly_consumption)

    def _validate_rate(self, value):
        if not callable(getattr(value, 'calculate_monthly_payments')):
            raise ValueError("The rate object must have a 'calculate_monthly_payments' method.")
        return value
    
    def _validate_current_monthly_consumption(self, value):
        if not isinstance(value, list):
            raise ValueError("current_monthly_consumption must be a list")
        
        if len(value) != 12:
            raise ValueError("current_monthly_consumption list must contain 12 items")
        
        if not all(isinstance(item, int) for item in value):
            raise ValueError("All items in current_monthly_consumption must be integers")
        
        return value
    
    def _validate_pv_system(self, value):
        if not isinstance(value, PVSystem):
            raise ValueError("pv_system must be an instance of PVSystem")
        return value
    
    @property
    def rate(self):
        return self._rate
    
    @rate.setter
    def rate(self, value):
        self._rate = self._validate_rate(value)
        self._current_payment = self._rate.calculate_monthly_payments(self._current_monthly_consumption)
    
    @property
    def current_monthly_consumption(self):
        return self._current_monthly_consumption
    
    @current_monthly_consumption.setter
    def current_monthly_consumption(self, value):
        self._current_monthly_consumption = self._validate_current_monthly_consumption(value)
        self._current_payment = self._rate.calculate_monthly_payments(self._current_monthly_consumption)

    @property
    def current_payment(self):
        return self._current_payment
    
    def calculate_new_monthly_consumption(self, pv_system):
        pv_system = self._validate_pv_system(pv_system)
        monthly_production = pv_system.calculate_annual_energy_production()
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
    
    def calculate_new_monthly_payment(self, pv_system):
        pv_system = self._validate_pv_system(pv_system)
        return self.rate.calculate_monthly_payments(self.calculate_new_monthly_consumption(pv_system))
