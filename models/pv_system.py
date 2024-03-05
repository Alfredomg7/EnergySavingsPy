from models.pv_module import PVModule
from models.location import Location

class PVSystem:
    def __init__(self, pv_module, pv_module_count, efficiency, location):
        self._pv_module = self.validate_pv_module(pv_module)
        self._pv_module_count = self.validate_pv_module_count(pv_module_count)
        self._efficiency = self.validate_efficiency(efficiency)
        self._location = self.validate_location(location)
        self._system_size = self.calculate_system_size()
    
    def validate_pv_module(self, value):
        if not isinstance(value, PVModule):
            raise ValueError("pv_module must be an instance of PVModule")
        return value
    
    def validate_pv_module_count(self, value):
        if not (isinstance(value, int) and value > 0):
            raise ValueError("pv module count must be an integer greater than 0")
        return value
    
    def validate_efficiency(self, value):
        if not 0.1 <= value <= 1:
            raise ValueError("Efficiency must be between 0.1 and 1")
        return value

    def validate_location(self, value):
        if not isinstance(value, Location):
            raise ValueError("location must be an instance of Location")
        return value
    
    def calculate_system_size(self):
        return self.pv_module._capacity * self._pv_module_count

    @property
    def pv_module(self):
        return self._pv_module
    
    @pv_module.setter
    def pv_module(self, value):
        self._pv_module = self.validate_pv_module(value)
        self._system_size = self.calculate_system_size()

    @property
    def pv_module_count(self):
        return self._pv_module_count
    
    @pv_module_count.setter
    def pv_module_count(self, value):
        self._pv_module_count = self.validate_pv_module_count(value)
        self._system_size = self.calculate_system_size()
    
    @property
    def efficiency(self):
        return self._efficiency
    
    @efficiency.setter
    def efficiency(self, value):
        self._efficiency = self.validate_efficiency(value)

    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        self._location = self.validate_location(value)
    
    @property
    def system_size(self):
        return self._system_size
    
    def calculate_annual_energy_production(self):
        annual_production = []
        solar_hours = self._location.get_solar_hours(self.pv_module.tilt_angle)
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if solar_hours:
            for month, hours in enumerate(solar_hours):
                days = days_in_month[month]
                monthly_production = round(self._system_size * hours * days * self._pv_module.efficiency * self._efficiency, 2)
                annual_production.append(monthly_production)
        return annual_production 
    
    

    