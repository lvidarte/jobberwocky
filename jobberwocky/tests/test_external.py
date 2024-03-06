import unittest
from unittest.mock import patch, Mock

from requests.exceptions import RequestException

import schemas
from external import ExternalAPI


class TestJobs(unittest.TestCase):

    def setUp(self):
        self.external_api = ExternalAPI()

    @patch('requests.get')
    def test_jobs(self, mock_requests_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            [
                "Jr Java Developer",
                24000,
                "Argentina",
                ["Java", "OOP"]
            ],
            [
                "Jr PHP Developer",
                24000,
                "Spain",
                ["PHP", "OOP"]
            ],
        ]

        mock_requests_get.return_value = mock_response

        result = self.external_api.jobs()

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], schemas.Job)

    @patch('requests.get')
    def test_jobs_with_filters(self, mock_requests_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            [
                "Jr Python Developer",
                28000,
                "USA",
                ["Python", "OOP"]
            ]
        ]

        mock_requests_get.return_value = mock_response

        result = self.external_api.jobs(name='python', country='usa')

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], schemas.Job)
        self.assertIn('name=python', result[0].uri)
        self.assertIn('country=usa', result[0].uri)

    @patch('requests.get')
    def test_jobs_raises_error(self, mock_requests_get):
        mock_requests_get.side_effect = RequestException()

        result = self.external_api.jobs()

        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])
