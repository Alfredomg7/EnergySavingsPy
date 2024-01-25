from database import SolarHoursData

class Location:
    def __init__(self, name, solar_hours_data=None):
        self.name = name
        self.solar_hours_data = solar_hours_data or SolarHoursData()

    def get_solar_hours(self, tilt):
        solar_hours = self.solar_hours_data.get_solar_hours(self.name, tilt)
        return solar_hours if solar_hours else None
        