from database.solar_hours_data import SolarHoursData
from database.location_data import LocationData

class Location:
    def __init__(self, name, solar_hours_data=None, location_data=None):
        self._name = name
        self._solar_hours_data = solar_hours_data or SolarHoursData()
        self._location_data = location_data or LocationData()
        self._region = self._location_data.get_region(self.name)
        self._region_id = self._location_data.get_region_id(self.name)
        self._residential_rate = self._location_data.get_residential_rate(self.name)
        self._summer_start_month = self._location_data.get_summer_start_month(self.name)

    @property
    def name(self):
        return self._name
    
    @property
    def region(self):
        return self._region
    
    @property
    def region_id(self):
        return self._region_id
    
    @property
    def residential_rate(self):
        return self._residential_rate
    
    @property
    def summer_start_month(self):
        return self._summer_start_month
    
    def get_solar_hours(self, tilt):
        solar_hours = self._solar_hours_data.get_solar_hours(self._name, tilt)
        return solar_hours if solar_hours else None

        