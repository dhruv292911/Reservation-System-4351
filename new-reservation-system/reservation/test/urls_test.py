import unittest

from booking.urls import *

class reservation_tests(unittest.TestCase):
    def test_urls_expected_size(self):
        self.assertTrue(len(urlpatterns) == 4)
        
if __name__ == '__main__': 
    unittest.main()
