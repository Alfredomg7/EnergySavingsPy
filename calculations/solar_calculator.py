class SolarSavingsCalculator:
    def __init__(self, rate, current_monthly_consumption):
        self.rate = rate
        self.current_monthly_consumption = current_monthly_consumption

    def calculate_new_monthly_consumption(self, pv_system):
        monthly_production = pv_system.calculate_energy_production()
        new_monthly_consumption = []
        
        for current_consumption, production in zip(self.current_monthly_consumption, monthly_production):
            new_consumption = max(current_consumption - production, 0)
            new_monthly_consumption.append(new_consumption)
        
        return new_monthly_consumption
        