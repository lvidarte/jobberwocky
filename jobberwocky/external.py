import logging
from dataclasses import dataclass
from urllib.parse import urlencode
from typing import Optional, List

import requests
from fastapi import Query

import config
import schemas


logger = logging.getLogger(f"{config.APP_NAME}.{__name__}")


@dataclass
class ExternalAPI:

    url_api: str = Query(config.EXTERNAL_API_URL, include_in_schema=False)

    def jobs(
        self,
        name: Optional[str] = None,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        country: Optional[str] = None,
    ) -> List[schemas.Job]:

        params = {
            'name': name,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'country': country,
        }
        url = self._get_full_url(params)
        logger.debug(f"Getting external jobs from {url}")
        try:
            response = requests.get(url)
            return [
                schemas.Job(
                    title=data[0],
                    salary=data[1],
                    country=data[2],
                    skills=data[3],
                    contact=None,
                    internal=False,
                    uri=url,
                )
                for data in response.json()
            ]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting jobs for external API: {e}")
            return []

    def _get_full_url(self, params: dict) -> str:
        _params = {
            key: value for key, value in params.items()
            if value is not None
        }
        if _params:
            return f"{self.url_api}?{urlencode(_params)}"
        else:
            return f"{self.url_api}"
