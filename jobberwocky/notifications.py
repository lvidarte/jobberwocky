import logging

import requests

import config
import schemas
import datamanager


logger = logging.getLogger(f"{config.APP_NAME}.{__name__}")


def notify(job: schemas.Job) -> None:
    logger.debug(f"Job: {job}")
    for subscription in datamanager.subscriptions().filter(job):
        logger.debug(f"Matched subscription: {subscription}")
        logger.info(f"Sending notification to {subscription.email} for {job.uri}")
        if config.MAILGUN_DOMAIN and config.MAILGUN_API_KEY:
            send_email(subscription.email, job.uri)


def send_email(email: str, job_uri: str) -> None:
    logger.info(f"Sending email to {email}")
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{config.MAILGUN_DOMAIN}/messages",
            auth=("api", config.MAILGUN_API_KEY),
            data={
                "from": f"{config.APP_NAME.capitalize()} <mailgun@{config.MAILGUN_DOMAIN}>",
                "to": [email],
                "subject": f"{config.APP_NAME.capitalize()} - This job is for you!",
                "text": f"This new job matches your search criteria: {job_uri}"
            }
        )
    except requests.HTTPError as e:
        logger.error(f"Error sending notification to {email}")
