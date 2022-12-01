import unittest

from booking.apps import *

class reservation_tests(unittest.TestCase):
    def test_canary(self):
        self.assertTrue(True)

    def test_apps_name(self):
        self.assertTrue(BookingConfig.name == 'booking')
        
    def test_apps_default(self):
        self.assertTrue(BookingConfig.default_auto_field == 'django.db.models.BigAutoField')

if __name__ == '__main__': 
    unittest.main()
