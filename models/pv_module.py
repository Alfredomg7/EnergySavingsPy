class PVModule:
    def __init__(self, capacity, tilt_angle, efficiency, lifespan=25, annual_degradation=0.005):
        self._capacity = self.validate_capacity(capacity)
        self._tilt_angle = self.validate_tilt_angle(tilt_angle)
        self._efficiency = self.validate_efficiency(efficiency)
        self._lifespan = self.validate_lifespan(lifespan)
        self._annual_degradation = self.validate_annual_degradation(annual_degradation)

    def validate_capacity(self, value):
        if not 0.01 <= value <= 1:
            raise ValueError("Capacity must be between 0.01 and 1")
        return value
    
    def validate_tilt_angle(self, value):
        if not 0 <= value <= 90:
            raise ValueError("Tilt angle must be between 0 and 90")
        return value

    def validate_efficiency(self, value):
        if not 0.1 <= value <= 1:
            raise ValueError("Efficiency must be between 0.1 and 1")
        return value
            
    def validate_lifespan(self, value):
        if not (isinstance(value, int) and 1 <= value <= 30):
            raise ValueError("Lifespan must be an integer between 1 and 30")
        return value

    def validate_annual_degradation(self, value):
        if not 0 <= value <= 0.1:
            raise ValueError("Annual degradation must be between 0 and 0.1")
        return value
            
    @property
    def capacity(self):
        return self._capacity
    
    @capacity.setter
    def capacity(self, value):
        self._capacity = self.validate_capacity(value)

    @property
    def tilt_angle(self):
        return self._tilt_angle
    
    @tilt_angle.setter
    def tilt_angle(self, value):
        self._tilt_angle = self.validate_tilt_angle(value)
    
    @property
    def efficiency(self):
        return self._efficiency
    
    @efficiency.setter
    def efficiency(self, value):
        self._efficiency = self.validate_efficiency(value)
    
    @property
    def lifespan(self):
        return self._lifespan
    
    @lifespan.setter
    def lifespan(self, value):
        self._lifespan = self.validate_lifespan(value)
    
    @property
    def annual_degradation(self):
        return self._annual_degradation
    
    @annual_degradation.setter
    def annual_degradation(self, value):
        self._annual_degradation = self.validate_annual_degradation(value)