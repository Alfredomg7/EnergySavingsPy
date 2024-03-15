from database.solar_hours_data import SolarHoursData
from database.location_data import LocationData

class Location:
    def __init__(self, name, solar_hours_data=None, location_data=None):
        self._name = name
        self._solar_hours_data = solar_hours_data or SolarHoursData()
        self._location_data = location_data or LocationData()
        self._region = self._location_data.get_region(self.name)

    @property
    def name(self):
        return self._name
    
    @property
    def region(self):
        return self._region
    
    def get_solar_hours(self, tilt):
        solar_hours = self._solar_hours_data.get_solar_hours(self._name, tilt)
        return solar_hours if solar_hours else None

        