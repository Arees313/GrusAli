import sys
import unittest
from unittest.mock import patch
import json
import datetime
import pandas as pd
import requests
from app import app, fetch_weather_data  # Import your Flask app and function

class TestSMHIAPIIntegration(unittest.TestCase):

    @patch('requests.get')
    def test_api_successful(self, mock_get):
        mock_response = {
            'timeSeries': [{
                'parameters': [
                    {'unit': 'Cel', 'values': [15]},
                    {'name': 'pcat', 'values': [0.5]}
                ]
            }]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(mock_response)
        weather_data = fetch_weather_data()
        self.assertIsInstance(weather_data, pd.DataFrame)
        self.assertGreater(len(weather_data), 0)

    @patch('requests.get')
    def test_api_500_error(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = 'Internal Server Error'
        with self.assertRaises(Exception):
            fetch_weather_data()

    @patch('requests.get')
    def test_api_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        with self.assertRaises(requests.exceptions.Timeout):
            fetch_weather_data()

    @patch('requests.get')
    def test_api_invalid_json(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "invalid json"
        with self.assertRaises(ValueError):
            fetch_weather_data()

    @patch('requests.get')
    def test_api_invalid_structure(self, mock_get):
        mock_response = {
            'timeSeries': [{
                'parameters': [
                    {'unit': 'Cel', 'values': [15]},
                    {'name': 'pcat', 'values': ['invalid']}
                ]
            }]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(mock_response)
        weather_data = fetch_weather_data()
        self.assertEqual(weather_data.iloc[0]['Regn (True/False)'], False)

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create a test client for Flask app
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Vederdata', response.data)  # Checks if the expected content is in the response

if __name__ == '__main__':
    unittest.main()
