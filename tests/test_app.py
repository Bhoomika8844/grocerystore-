import unittest
from app import app

class GroceryStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login')
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
