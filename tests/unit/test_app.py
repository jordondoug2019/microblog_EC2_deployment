#import unittest
import pytest
import sys
import os
sys.path.append(os.getcwd())
from microblog import app

@pytest.fixture
def client():
    app.config.update({"TESTING": True,})
    return app.test_client()

def test_website(client):
    response = client.get("/", follow_redirects = True)
    assert response.status_code == 200


#class TestLoginFunction(unittest.TestCase):

 #   def test_successful_login(self):
 
  #      username = "john_doe"
   #     password = "password123"
#
 #       expected_result = "Login successful"

  #      result = login(username, password)

   #     self.assertEqual(result, expected_result)

#if __name__ == "__main__":
 #   unittest.main()
