import logging
from typing import List

from fastapi import (
    FastAPI,
    HTTPException,
    BackgroundTasks,
    Depends,
    Query,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import config
import models
import schemas
import datamanager
import external
import notifications


app = FastAPI(
    title=f"{config.APP_NAME.capitalize()} API 🚀",
    description=(
        "A service that works as a store for job opportunities, "
        "where companies can share open positions."
    ),
    version="0.0.1",
    contact={
        "name": "Leo Vidarte",
        "url": "https://minirobots.com.ar",
        "email": "lvidarte@gmail.com",
    }
)
logger = logging.getLogger(f"{config.APP_NAME}.{__name__}")


@app.get('/', include_in_schema=False)
def home():
    return {
        "message": f"Welcome to the {config.APP_NAME.capitalize()} API",
        "version": f"{config.APP_VERSION}",
    }


@app.get('/favicon.ico', include_in_schema=False)
def favicon():
    return FileResponse('favicon.png')


@app.post('/jobs', status_code=201)
def create_job(
    job: schemas.Job,
    background_tasks: BackgroundTasks,
    jobs: datamanager.Jobs = Depends(datamanager.jobs),
) -> dict:
    new_job: schemas.Job = jobs.create(job)
    background_tasks.add_task(notifications.notify, new_job)
    return {
        "status": True,
        "message": "Job created.",
        "data": new_job,
    }


@app.get('/jobs/{job_id}')
def get_job(
    job_id: int,
    jobs: datamanager.Jobs = Depends(datamanager.jobs),
) -> schemas.Job:
    try:
        job: schemas.Job = jobs.get(job_id)
        return job
    except:
        raise HTTPException(status_code=404, detail="Job not found.")


@app.get('/jobs')
def get_jobs(
    title: str = Query(None),
    salary_min: int = Query(None),
    salary_max: int = Query(None),
    country: str = Query(None),
    jobs: datamanager.Jobs = Depends(datamanager.jobs),
    external_api: external.ExternalAPI = Depends(external.ExternalAPI),
) -> List[schemas.Job]:
    internal_jobs = jobs.all(title, salary_min, salary_max, country)
    external_jobs = external_api.jobs(title, salary_min, salary_max, country)
    return sorted(internal_jobs + external_jobs, key=lambda job: job.title)


@app.post('/subscriptions', status_code=201)
def create_subscription(
    subscription: schemas.Subscription,
    subscriptions: datamanager.Subscriptions = Depends(datamanager.subscriptions),
) -> dict:
    new_subscription: schemas.Subscription = subscriptions.create(subscription)
    return {
        "status": True,
        "message": "Subscription created.",
        "data": new_subscription,
    }


@app.get('/subscriptions')
def get_subscriptions(
    subscriptions: datamanager.Subscriptions = Depends(datamanager.subscriptions),
) -> List[schemas.Subscription]:
    return subscriptions.all()
