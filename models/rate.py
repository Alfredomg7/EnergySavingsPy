from models.location import Location
from utils.date_utils import generate_days_in_month

class Rate:
    IVA_RATE = 1.08

    def __init__(self, location, end_year_month, needs_days_in_month=False):
        self._location = self._validate_location(location)
        self._end_year_month = end_year_month
        self._charges = None
        self._needs_days_in_month = needs_days_in_month

    def _validate_location(self, value):
        if not isinstance(value, Location):
            raise ValueError("The location object must be an instance of Location")
        return value

    def _validate_charges(self, values):
        if not values:
            raise ValueError("Charges data is not available")
        
        if not isinstance(values, list):
            raise ValueError("Charges data must be a list")

        if len(values) != 12:
            raise ValueError(f"Charges data list must contain data for 12 months")

        if not all(isinstance(item, dict) for item in values):
            raise ValueError("Each item in charges data must be a dictionary")

        return values
    
    def _validate_monthly_values(self, values, name):
        if not isinstance(values, list):
            raise ValueError(f"{name} must be a list")
        
        if len(values) != 12:
            raise ValueError(f"{name} list must contain 12 items")
        
        if not all(item >= 0 for item in values):
            raise ValueError(f"All items in {name} must be positive numbers")
        
        return values
    
    def _validate_monthly_parameters(self, parameters):
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a dictionary")
        
        for key, value in parameters.items():
            self._validate_monthly_values(value, key)
        
        return parameters
    
    def calculate_monthly_payments(self, monthly_consumption, **kwargs):
        if self._needs_days_in_month:
            days_in_months = generate_days_in_month(self._end_year_month)
        
        monthly_consumption = self._validate_monthly_values(monthly_consumption, "monthly_consumption")
        kwargs = self._validate_monthly_parameters(kwargs)
        
        if self._needs_days_in_month:
            return [
                self._calculate_payment(charge, consumption, days_in_month, **{k: v[i] for k, v in kwargs.items()})
                for i, (charge, consumption, days_in_month) in enumerate(zip(self._charges, monthly_consumption, days_in_months))
            ]
        else:
            return [
                self._calculate_payment(charge, consumption, **{k: v[i] for k, v in kwargs.items()})
                for i, (charge, consumption) in enumerate(zip(self._charges, monthly_consumption))
            ]

    def _calculate_payment(self, charge, consumption, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")