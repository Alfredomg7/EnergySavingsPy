from abc import ABC, abstractmethod

class SolarHoursDAO(ABC):
    @abstractmethod
    def get_solar_hours(self, location_name, tilt):
        pass

class PdbtRateDAO(ABC):
    @abstractmethod
    def get_charges(self, region_id, end_year_month):
        pass

class ResidentialRatesDAO(ABC):
    @abstractmethod
    def get_summer_charges(self, rate, summer_months, end_year_month):
        pass

    def get_winter_charges(self, rate, winter_months, end_year_month):
        pass
    
class LocationDAO(ABC):
    @abstractmethod
    def get_region(self, location_name):
        pass

    @abstractmethod
    def get_region_id(self, location_name):
        pass

    @abstractmethod
    def get_summer_start_month(self, location_name):
        pass