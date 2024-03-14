from models.pv_module import PVModule
from models.location import Location

class PVSystem:
    def __init__(self, pv_module, pv_module_count, efficiency, location):
        self._pv_module = self._validate_pv_module(pv_module)
        self._pv_module_count = self._validate_pv_module_count(pv_module_count)
        self._efficiency = self._validate_efficiency(efficiency)
        self._location = self._validate_location(location)
        self._system_size = self._calculate_system_size()
        self._invalidate_caches()

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
    
    def _validate_cost_per_kw(self, value):
        if not value > 0:
            raise ValueError("Cost per kW must be greater than 0")
        return value
    
    def _calculate_system_size(self):
        return self._pv_module.capacity * self._pv_module_count

    def _invalidate_caches(self):
        self._installation_cost_cache = None
        self._monthly_energy_production_cache = None
        self._lifetime_production_cache = None
    
    @property
    def pv_module(self):
        return self._pv_module
    
    @pv_module.setter
    def pv_module(self, value):
        self._pv_module = self._validate_pv_module(value)
        self._system_size = self._calculate_system_size()
        self._invalidate_caches()

    @property
    def pv_module_count(self):
        return self._pv_module_count
    
    @pv_module_count.setter
    def pv_module_count(self, value):
        self._pv_module_count = self._validate_pv_module_count(value)
        self._system_size = self._calculate_system_size()
        self._invalidate_caches()

    @property
    def efficiency(self):
        return self._efficiency
    
    @efficiency.setter
    def efficiency(self, value):
        self._efficiency = self._validate_efficiency(value)
        self._invalidate_caches()
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        self._location = self._validate_location(value)
        self._invalidate_caches()

    @property
    def system_size(self):
        return self._system_size

    def calculate_installation_cost(self, cost_per_kw=None):
        if self._installation_cost_cache is not None and cost_per_kw is None:
            return self._installation_cost_cache
        
        default_cost_per_kw = 20000
        cost_per_kw = self._validate_cost_per_kw(cost_per_kw) if cost_per_kw else default_cost_per_kw
        installation_cost = cost_per_kw * self._system_size
        
        self._installation_cost_cache = installation_cost
        return installation_cost
    
    def calculate_monthly_energy_production(self):
        if self._monthly_energy_production_cache is not None:
            return self._monthly_energy_production_cache
        
        annual_production = []
        solar_hours = self._location.get_solar_hours(self._pv_module.tilt_angle)
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if solar_hours:
            for month, hours in enumerate(solar_hours):
                days = days_in_month[month]
                monthly_production = round(self._system_size * hours * days * self._pv_module.efficiency * self._efficiency, 2)
                annual_production.append(monthly_production)
        
        self._monthly_energy_production_cache = annual_production
        return annual_production 
    
    def calculate_lifetime_production(self):
        if self._lifetime_production_cache is not None:
            return self._lifetime_production_cache
        
        annual_production = sum(self.calculate_monthly_energy_production())
        degradation_factor = 1 - self._pv_module.annual_degradation
        lifetime_production = [round((annual_production * (degradation_factor ** year)), 2) for year in range(self._pv_module.lifespan)]
        
        self._lifetime_production_cache = lifetime_production
        return lifetime_production

    