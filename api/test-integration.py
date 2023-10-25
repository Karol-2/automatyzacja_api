import unittest
import requests
import time


class TestAppIntegration(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://app:5000'
        self.resource_key = 'integration_key'

    def test_crud_resource(self):
        # Tworzenie zasobu
        response = requests.post(f'{self.base_url}/resource',
                                 json={'key': self.resource_key, 'value': 'integration_value'})
        self.assertEqual(response.status_code, 201)

        # Odczyt zasobu
        response = requests.get(f'{self.base_url}/resource/{self.resource_key}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['key'], self.resource_key)

        # Aktualizacja zasobu
        response = requests.put(f'{self.base_url}/resource/{self.resource_key}',
                                json={'value': 'updated_integration_value'})
        self.assertEqual(response.status_code, 200)

        # Usunięcie zasobu
        response = requests.delete(f'{self.base_url}/resource/{self.resource_key}')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
