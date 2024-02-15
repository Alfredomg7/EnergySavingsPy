class SolarSavingsCalculator:
    def __init__(self, rate, current_monthly_consumption):
        self.rate = rate
        self.current_monthly_consumption = current_monthly_consumption

    def calculate_new_monthly_consumption(self, pv_system):
        monthly_production = pv_system.calculate_energy_production()
        new_monthly_consumption = []
        energy_bank = 0

        for current_consumption, production in zip(self.current_monthly_consumption, monthly_production):
            energy_balance = production - current_consumption
            if energy_balance >= 0:
                # Save surplus energy to the bank
                energy_bank += energy_balance
                new_monthly_consumption.append(0)
            else:
                # Calculate the deficit after using the bank's energy
                deficit_after_bank = energy_bank + energy_balance
                if deficit_after_bank >= 0:
                    # Bank covers the entire deficit
                    energy_bank = deficit_after_bank
                    new_monthly_consumption.append(0)
                else:
                    # Bank cannot cover the entire deficit
                    new_monthly_consumption.append(round(abs(deficit_after_bank),2))
                    energy_bank = 0

        # Loop again if there is remaining energy in the bank
        if energy_bank > 0:
            for i in range(len(new_monthly_consumption)):
                if new_monthly_consumption[i] > 0 and energy_bank > 0:
                    if new_monthly_consumption[i] <= energy_bank:
                        energy_bank -= new_monthly_consumption[i]
                        new_monthly_consumption[i] = 0
                    else:
                        new_monthly_consumption[i] -= energy_bank
                        energy_bank = 0

        return new_monthly_consumption