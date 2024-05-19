import unittest
from utils.date_utils import *

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
            extract_month('2023-May')

    def test_extract_year(self):
        self.assertEqual(extract_year('2023-09'), 2023)
        self.assertEqual(extract_year('2021-11'), 2021)
        with self.assertRaises(ValueError):
            extract_year('2021-Feb')

    def test_generate_months(self):
        self.assertEqual(generate_months(1), [1, 2, 3, 4, 5, 6])
        self.assertEqual(generate_months(9), [9, 10, 11, 12, 1, 2])
        with self.assertRaises(TypeError):
            generate_months('6')
    
    def test_get_winter_start_month(self):
        self.assertEqual(get_winter_start_month(1), 7)
        self.assertEqual(get_winter_start_month(9), 3)
        with self.assertRaises(TypeError):
            get_winter_start_month('7')
    
    def test_generate_days_in_month(self):
        self.assertEqual(generate_days_in_month(6, 2022), [30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31])
        self.assertEqual(generate_days_in_month(1, 2024), [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
        with self.assertRaises(TypeError):
            generate_days_in_month('6', '2022')
            
if __name__ == '__main__':
    unittest.main()
