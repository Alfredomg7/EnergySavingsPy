from database.solar_hours_data import SolarHoursData
from database.location_data import LocationData

class Location:
    def __init__(self, name, solar_hours_data=None, location_data=None):
        self.name = name
        self.solar_hours_data = solar_hours_data or SolarHoursData()
        self.location_data = location_data or LocationData()

    def get_solar_hours(self, tilt):
        solar_hours = self.solar_hours_data.get_solar_hours(self.name, tilt)
        return solar_hours if solar_hours else None
    
    def get_state(self):
        state = self.location_data.get_state(self.name)
        return state if state else None

        