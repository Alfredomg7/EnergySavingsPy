from database.residential_rates_data import ResidentialRatesData
from utils.date_utils import generate_months, get_winter_start_month, extract_month
from models.rate import Rate

class ResidentialRate(Rate):
    # Dictionaries with energy charge tiers for each residential rate
    # For summer season 'excess' tier applies when the consumption exceeds the high intermediate tier
    energy_summer_charge_tiers = {'1C': {'basic': 150, 'low_intermediate': 300, 'high_intermediate': 450},
                                  '1D': {'basic': 175, 'low_intermediate': 400, 'high_intermediate': 600},
                                  '1E': {'basic': 300, 'low_intermediate': 750, 'high_intermediate': 900},
                                  '1F': {'basic': 300, 'low_intermediate': 1200, 'high_intermediate': 2500}}

    # For winter season 'excess' tier applies when the consumption exceeds the intermediate tier
    energy_winter_charge_tiers = {'1C': {'basic': 75, 'intermediate': 175},
                                  '1D': {'basic': 75, 'intermediate': 200},
                                  '1E': {'basic': 75, 'intermediate': 200},
                                  '1F': {'basic': 75, 'intermediate': 200}}
    
    def __init__(self, location, end_year_month, residential_rates_data=None):
        super().__init__(location, end_year_month)
        self._rate = self._location.residential_rate
        self._summer_start_month = self._validate_summer_start_month(self._location.summer_start_month)
        self._summer_months = generate_months(self._summer_start_month)
        self._winter_start_month = get_winter_start_month(self._summer_start_month)
        self._winter_months = generate_months(self._winter_start_month)
        self._residential_rates_data = residential_rates_data or ResidentialRatesData()
        self._charges = self._get_charges()
    
    def _validate_summer_start_month(self, value):
        if not isinstance(value, int):
            raise ValueError("Summer start month must be an integer")

        # Summer season can start on February thru May according to CFE website
        first_month = 2
        last_month = 5
        if value not in [i for i in range(first_month, last_month+1)]:
            raise ValueError(f"Summer start month must be between {min} and {max}")
        
        return value
    
    def _get_charges(self):
        charges = self._residential_rates_data.get_charges(self._rate, self._summer_months, self._winter_months, self._end_year_month)
        charges = self._validate_charges(charges)
        return charges
    
    def _calculate_payment(self, charge, consumption):
        # When consumption is less than 25 kWh CFE charges the equivalent of 25 kWh consumption as fix charge
        consumption = max(consumption, 25)
        current_month = extract_month(charge['billing_period'])
        is_summer = current_month in self._summer_months
        charge_tiers = self.energy_summer_charge_tiers[self._rate] if is_summer else self.energy_winter_charge_tiers[self._rate]

        for tier in sorted(charge_tiers.keys(), key=lambda k: charge_tiers[k]):
            if consumption <= charge_tiers[tier]:
                payment = consumption * charge[tier]
                break
        else:
            payment = consumption * charge['excess']

        payment = round(payment * self.IVA_RATE, 2)
        return payment