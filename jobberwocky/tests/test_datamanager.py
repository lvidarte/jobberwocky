import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm.exc import NoResultFound

import datamanager
import models
import schemas


class TestJobs(unittest.TestCase):

    def setUp(self):
        self.job = models.Job(
            title="Python Developer",
            salary=35000,
            country="USA",
            skills=["python"],
            contact="jobs@avature.net",
        ) 

    def test_all(self):
        MockSession = MagicMock()
        MockSession.__enter__.return_value.query.return_value.all.return_value = [self.job]

        MockDatabase = MagicMock()
        MockDatabase.return_value.session.return_value = MockSession

        jobs = datamanager.Jobs(MockDatabase())

        result = jobs.all()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], schemas.Job)
        self.assertEqual(result[0].title, "Python Developer")

    def test_all_with_filters(self):
        MockSession = MagicMock()
        MockSession.__enter__.return_value.query.return_value.filter.return_value.all.return_value = [self.job]

        MockDatabase = MagicMock()
        MockDatabase.return_value.session.return_value = MockSession

        jobs = datamanager.Jobs(MockDatabase())

        result = jobs.all(title="python")

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], schemas.Job)
        self.assertEqual(result[0].title, "Python Developer")

    def test_get(self):
        MockSession = MagicMock()
        MockSession.__enter__.return_value.query.return_value.filter.return_value.first.return_value = self.job

        MockDatabase = MagicMock()
        MockDatabase.return_value.session.return_value = MockSession

        jobs = datamanager.Jobs(MockDatabase())

        result = jobs.get(job_id=1)

        self.assertIsInstance(result, schemas.Job)
        self.assertEqual(result.title, "Python Developer")

    def test_get_raises_error(self):
        MockSession = MagicMock()
        MockSession.__enter__.return_value.query.return_value.filter.side_effect = NoResultFound()

        MockDatabase = MagicMock()
        MockDatabase.return_value.session.return_value = MockSession

        jobs = datamanager.Jobs(MockDatabase())

        with self.assertRaises(NoResultFound):
            jobs.get(job_id=1)

    def test_create(self):
        MockSession = MagicMock()

        MockDatabase = MagicMock()
        MockDatabase.return_value.session.return_value = MockSession

        jobs = datamanager.Jobs(MockDatabase())

        job = schemas.Job(
            title="Sr Golang Developer",
            salary=40000,
            country="Argentina",
            skills=["concurrency"],
        )
        result = jobs.create(job)

        MockSession.__enter__.return_value.add.assert_called_once()
        MockSession.__enter__.return_value.commit.assert_called_once()
        MockSession.__enter__.return_value.refresh.assert_called_once()

        self.assertIsInstance(result, schemas.Job)
        self.assertEqual(result.title, "Sr Golang Developer")


class TestSubscriptions(unittest.TestCase):

    def setUp(self):
        self.subscription = schemas.Subscription(
            email="myname@someserver.net",
            title="golang",
            salary_min=30000,
            country="arg",
        )

    def test_create(self):
        MockSession = MagicMock()

        MockDatabase = MagicMock()
        MockDatabase.return_value.session.return_value = MockSession

        subscriptions = datamanager.Subscriptions(MockDatabase())

        result = subscriptions.create(self.subscription)

        MockSession.__enter__.return_value.add.assert_called_once()
        MockSession.__enter__.return_value.commit.assert_called_once()
        MockSession.__enter__.return_value.refresh.assert_called_once()

        self.assertIsInstance(result, schemas.Subscription)
        self.assertEqual(result.email, "myname@someserver.net")
        self.assertEqual(result.title, "golang")
        self.assertEqual(result.salary_min, 30000)
        self.assertEqual(result.country, "arg")

    def test_filter(self):
        MockSession = MagicMock()
        MockSession.__enter__.return_value.query.return_value.all.return_value = [self.subscription]

        MockDatabase = MagicMock()
        MockDatabase.return_value.session.return_value = MockSession

        subscriptions = datamanager.Subscriptions(MockDatabase())

        job = schemas.Job(
            title="Sr Golang Developer",
            salary=35000,
            country="Argentina",
            skills=["oop", "coroutines"],
            contact="jobs@avature.net",
        )

        result = subscriptions.filter(job)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], schemas.Subscription)
        self.assertEqual(result[0].email, "myname@someserver.net")
        self.assertEqual(result[0].title, "golang")
        self.assertEqual(result[0].salary_min, 30000)
        self.assertEqual(result[0].country, "arg")
