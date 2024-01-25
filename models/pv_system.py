class PVModule:
    def __init__(self, capacity, tilt_angle, efficiency, lifespan=25, annual_degradation=0.005):
        self.capacity = capacity
        self.tilt_angle = tilt_angle
        self.efficiency = efficiency
        self.lifespan = lifespan
        self.annual_degration = annual_degradation

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
        if solar_hours:
            for hours in solar_hours:
                monthly_energy = self.system_size * hours * self.pv_module.efficiency * self.efficiency
                monthly_production.append(monthly_energy)
        return monthly_production 
    
    

    