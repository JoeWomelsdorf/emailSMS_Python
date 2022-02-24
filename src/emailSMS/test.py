
from emailSMS import Manager
import unittest

class emailSMSTest(unittest.TestCase):

    def test_invalid_phone(self):
        self.assertRaises(TypeError, Manager('2','AT&T', "email@gmail.com", "pass"))

    def test_invalid_email(self):
        self.assertRaises(TypeError, Manager('2039499363','AT&T', "notanemail", "pass"))

    def test_invalid_carrier(self):
        self.assertRaises(KeyError, Manager('2039499363','notcarrier', "email@gmail.com", "pass"))

    
    
if __name__ == "__main__":
    unittest.main()