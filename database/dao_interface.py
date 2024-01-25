from abc import ABC, abstractmethod

class SolarHoursDAO(ABC):
    @abstractmethod
    def get_solar_hours(self, location_name, tilt):
        pass