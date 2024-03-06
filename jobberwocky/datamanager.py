import logging
from typing import Optional, List

from sqlalchemy.orm.exc import NoResultFound

import config
import models
import schemas
from database import Database


logger = logging.getLogger(f"{config.APP_NAME}.{__name__}")


class Jobs:

    def __init__(self, database: Database):
        self.database = database

    def create(self, job: schemas.Job) -> schemas.Job:
        with self.database.session() as session:
            _job = models.Job(**job.dict(exclude={'uri', 'internal'}))
            session.add(_job)
            session.commit()
            session.refresh(_job)
            return self._to_schema(_job)

    def all(
        self,
        title: Optional[str] = None,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        country: Optional[str] = None,
    ) -> List[schemas.Job]:
        with self.database.session() as session:
            query = session.query(models.Job)
            if title is not None:
                query = query.filter(models.Job.title.like(f"%{title}%"))
            if salary_min is not None:
                query = query.filter(models.Job.salary >= salary_min)
            if salary_max is not None:
                query = query.filter(models.Job.salary <= salary_max)
            if country is not None:
                query = query.filter(models.Job.country.like(f"%{country}%"))
            return [self._to_schema(job) for job in query.all()]

    def get(self, job_id: int) -> schemas.Job:
        with self.database.session() as session:
            query = session.query(models.Job)
            try:
                job = query.filter(models.Job.id == job_id).first()
                return self._to_schema(job)
            except NoResultFound:
                logger.error(f"Job {job_id} not found.")
                raise

    def _to_schema(self, job: models.Job) -> schemas.Job:
        """Converts from models.Job to schemas.Job"""
        _job = schemas.Job(**job.__dict__)
        _job.uri = f'{config.APP_URL}/jobs/{job.id}'
        return _job


def jobs() -> Jobs:
    return Jobs(Database())


class Subscriptions:

    def __init__(self, database: Database):
        self.database = database

    def create(self, subscription: schemas.Subscription) -> schemas.Subscription:
        with self.database.session() as session:
            _subscription = models.Subscription(**subscription.dict())
            session.add(_subscription)
            session.commit()
            session.refresh(_subscription)
            return self._to_schema(_subscription)

    def all(self) -> List[schemas.Subscription]:
        with self.database.session() as session:
            query = session.query(models.Subscription)
            return [self._to_schema(subscription) for subscription in query.all()]

    def filter(self, job: schemas.Job) -> List[schemas.Subscription]:
        with self.database.session() as session:
            subscriptions = []
            for subscription in session.query(models.Subscription).all():
                if subscription.title.lower() in job.title.lower() and \
                   subscription.country.lower() in job.country.lower() and \
                   subscription.salary_min <= job.salary:
                    subscriptions.append(self._to_schema(subscription))
            return subscriptions

    def _to_schema(self, subscription: models.Subscription) -> schemas.Subscription:
        """Converts from models.Subscription to schemas.Subscription"""
        _subscription = schemas.Subscription(**subscription.__dict__)
        return _subscription


def subscriptions() -> Subscriptions:
    return Subscriptions(Database())
