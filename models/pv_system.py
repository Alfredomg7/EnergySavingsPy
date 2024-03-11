from models.pv_module import PVModule
from models.location import Location

class PVSystem:
    def __init__(self, pv_module, pv_module_count, efficiency, location):
        self._pv_module = self._validate_pv_module(pv_module)
        self._pv_module_count = self._validate_pv_module_count(pv_module_count)
        self._efficiency = self._validate_efficiency(efficiency)
        self._location = self._validate_location(location)
        self._system_size = self._calculate_system_size()
        self._monthly_energy_production = self._calculate_monthly_energy_production()
    
    def _validate_pv_module(self, value):
        if not isinstance(value, PVModule):
            raise ValueError("pv_module must be an instance of PVModule")
        return value
    
    def _validate_pv_module_count(self, value):
        if not (isinstance(value, int) and value > 0):
            raise ValueError("pv module count must be an integer greater than 0")
        return value
    
    def _validate_efficiency(self, value):
        if not 0.1 <= value <= 1:
            raise ValueError("Efficiency must be between 0.1 and 1")
        return value

    def _validate_location(self, value):
        if not isinstance(value, Location):
            raise ValueError("location must be an instance of Location")
        return value
    
    def _calculate_system_size(self):
        return self._pv_module.capacity * self._pv_module_count

    @property
    def pv_module(self):
        return self._pv_module
    
    @pv_module.setter
    def pv_module(self, value):
        self._pv_module = self._validate_pv_module(value)
        self._system_size = self._calculate_system_size()
        self._monthly_energy_production = self._calculate_monthly_energy_production()

    @property
    def pv_module_count(self):
        return self._pv_module_count
    
    @pv_module_count.setter
    def pv_module_count(self, value):
        self._pv_module_count = self._validate_pv_module_count(value)
        self._system_size = self._calculate_system_size()
        self._monthly_energy_production = self._calculate_monthly_energy_production()

    @property
    def efficiency(self):
        return self._efficiency
    
    @efficiency.setter
    def efficiency(self, value):
        self._efficiency = self._validate_efficiency(value)
        self._monthly_energy_production = self._calculate_monthly_energy_production()
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        self._location = self._validate_location(value)
        self._monthly_energy_production = self._calculate_monthly_energy_production()

    @property
    def system_size(self):
        return self._system_size
    
    @property 
    def monthly_energy_production(self):
        return self._monthly_energy_production
     
    def _calculate_monthly_energy_production(self):
        annual_production = []
        solar_hours = self._location.get_solar_hours(self._pv_module.tilt_angle)
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if solar_hours:
            for month, hours in enumerate(solar_hours):
                days = days_in_month[month]
                monthly_production = round(self._system_size * hours * days * self._pv_module.efficiency * self._efficiency, 2)
                annual_production.append(monthly_production)
        return annual_production 
    
    def calculate_lifetime_production(self):
        annual_production = sum(self.monthly_energy_production)
        degradation_factor = 1 - self._pv_module.annual_degradation
        lifetime_production = [round((annual_production * (degradation_factor ** year)), 2) for year in range(self._pv_module.lifespan)]
        return lifetime_production

    