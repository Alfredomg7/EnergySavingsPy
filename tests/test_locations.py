import unittest
from models.location import Location

class TestLocation(unittest.TestCase):
    def setUp(self):
        self.test_city = 'Mexicali'
        self.invalid_city = 'Atlantis'
        self.location = Location(self.test_city)

    def test_get_state(self):
        # Testing with a valid city
        state = self.location.state
        self.assertIsNotNone(state, f"State should exist for {self.test_city}")
        self.assertIsInstance(state, str, f"Expected state to be a string for {self.test_city}")

        # Testing with an invalid city
        invalid_location = Location(self.invalid_city)
        state = invalid_location.state
        self.assertIsNone(state, f"State should be None for an invalid city like {self.invalid_city}")

if __name__ == '__main__':
    unittest.main()