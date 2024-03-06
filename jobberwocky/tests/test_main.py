import unittest

from fastapi.testclient import TestClient

from main import app


class TestApiRoutes(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.client.headers["Content-Type"] = "application/json"

    def test_create_job_success(self):
        data = {
            "title": "Jr Java Developer",
            "salary": 24000,
            "country": "Argentina",
            "skills": ["Java", "OOP"],
            "contact": "jobs@avature.net",
        }
        response = self.client.post("/jobs/", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.json()["message"], "Job created.")
        self.assertEqual(response.json()["data"]["title"], data["title"])

    def test_create_job_error(self):
        data = {
            "title": "Jr Java Developer",
            "salary": "24000",
        }
        response = self.client.post("/jobs/", json=data)
        self.assertEqual(response.status_code, 422)

    def test_get_jobs(self):
        response = self.client.get("/jobs/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_job(self):
        data = {
            "title": "Sr Python Developer",
            "salary": 30000,
            "country": "Argentina",
            "skills": ["python", "unittest"],
            "contact": "jobs@avature.net",
        }
        response = self.client.post("/jobs/", json=data)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(response.json()["data"]["uri"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], data["title"])

    def test_get_job_not_found(self):
        response = self.client.get("/jobs/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Job not found.")

    def test_create_subscription(self):
        data = {
            "email": "myname@site.com", 
            "title": "python",
            "salary_min": 24000,
            "country": "arg",
        }
        response = self.client.post("/subscriptions/", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["status"])
        self.assertEqual(response.json()["message"], "Subscription created.")
        self.assertEqual(response.json()["data"]["email"], data["email"])

    def test_create_subscription_error(self):
        data = {
            "email": "myname@site.com", 
        }
        response = self.client.post("/subscriptions/", json=data)
        self.assertEqual(response.status_code, 422)

    def test_get_subscriptions(self):
        response = self.client.get("/subscriptions/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)


if __name__ == '__main__':
    unittest.main()
