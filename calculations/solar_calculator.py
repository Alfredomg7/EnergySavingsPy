class SolarSavingsCalculator:
    def __init__(self, rate, current_monthly_consumption):
        self.rate = rate
        self.current_monthly_consumption = current_monthly_consumption
        self.current_payment = rate.calculate_monthly_payments(current_monthly_consumption)

    def calculate_new_monthly_consumption(self, pv_system):
        monthly_production = pv_system.calculate_energy_production()
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
        return self.rate.calculate_monthly_payments(self.calculate_new_monthly_consumption(pv_system))
