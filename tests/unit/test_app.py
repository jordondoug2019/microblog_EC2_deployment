#!/usr/bin/env python
import unittest
from app import create_app
from app import db



class TestLoginFunction(unittest.TestCase):

    def test_successful_login(self):
 
        username = "john_doe"
        password = "password123"

        expected_result = "Login successful"

        result = login(username, password)

        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
