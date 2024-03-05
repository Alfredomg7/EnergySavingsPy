class PVSystem:
    def __init__(self, pv_module, pv_module_count, efficiency, location):
        self.pv_module = pv_module
        self.pv_module_count = pv_module_count
        self.system_size = self.calculate_system_size()
        self.efficiency = efficiency
        self.location = location
        
    def calculate_system_size(self):
        return self.pv_module.capacity * self.pv_module_count

    def calculate_energy_production(self):
        monthly_production = []
        solar_hours = self.location.get_solar_hours(self.pv_module.tilt_angle)
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if solar_hours:
            for month, hours in enumerate(solar_hours):
                days = days_in_month[month]
                monthly_energy = round(self.system_size * hours * days * self.pv_module.efficiency * self.efficiency, 2)
                monthly_production.append(monthly_energy)
        return monthly_production 
    
    

    