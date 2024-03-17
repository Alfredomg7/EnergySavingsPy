import unittest
from utils.date_utils import calculate_start_month, format_month, extract_month, extract_year

class TestDateUtils(unittest.TestCase):

    def test_calculate_start_month(self):
        self.assertEqual(calculate_start_month('2023-09'), '2022-10')
        self.assertEqual(calculate_start_month('2023-01'), '2022-02')
        with self.assertRaises(ValueError):
            calculate_start_month('2023-Jun')

    def test_format_month(self):
        self.assertEqual(format_month(2023, 9), '2023-09')
        self.assertEqual(format_month(2023, 11), '2023-11')
        with self.assertRaises(ValueError):
            format_month('2023', 'August')

    def test_extract_month(self):
        self.assertEqual(extract_month('2023-03'), 3)
        self.assertEqual(extract_month('2023-10'), 10)
        with self.assertRaises(ValueError):
            self.assertIsNone(extract_month('2023-May'))

    def test_extract_year(self):
        self.assertEqual(extract_year('2023-09'), 2023)
        self.assertEqual(extract_year('2021-11'), 2021)
        with self.assertRaises(ValueError):
            self.assertIsNone(extract_year('2021-Feb'))

if __name__ == '__main__':
    unittest.main()
