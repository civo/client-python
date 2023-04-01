import unittest

from civo.utils import filter_list

class TestFilterList(unittest.TestCase):
    def setUp(self):
        self.data = [
            {'name': 'John', 'age': 25},
            {'name': 'Jane', 'age': 30},
            {'name': 'Bob', 'age': 25},
        ]
        
    def test_filter_by_exact_match(self):
        filter_by = 'age:25'
        expected_result = [
            {'name': 'John', 'age': 25},
            {'name': 'Bob', 'age': 25},
        ]
        result = filter_list(self.data, filter_by)
        self.assertCountEqual(result, expected_result)
        
    def test_filter_by_partial_match(self):
        filter_by = 'name:J'
        expected_result = [
            {'name': 'John', 'age': 25},
            {'name': 'Jane', 'age': 30},
        ]
        result = filter_list(self.data, filter_by)
        self.assertCountEqual(result, expected_result)
        
    def test_filter_by_invalid_format(self):
        filter_by = 'invalid_format'
        with self.assertRaises(ValueError):
            filter_list(self.data, filter_by)
            
    def test_filter_by_invalid_key(self):
        filter_by = 'invalid_key:25'
        with self.assertRaises(KeyError):
            filter_list(self.data, filter_by)
        
if __name__ == '__main__':
    unittest.main()
