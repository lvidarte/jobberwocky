from typing import Optional

from pydantic import BaseModel


class Job(BaseModel):
    title: str
    salary: int
    country: str
    skills: list[str]
    contact: Optional[str] = None
    internal: Optional[bool] = True
    uri: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Sr Python Developer",
                    "salary": 50000,
                    "country": "Argentina",
                    "skills": ["Python", "OOP", "Unittest"],
                    "contact": "jobs@avature.net",
                }
            ]
        }
    }


class Subscription(BaseModel):
    email: str
    title: str
    salary_min: int
    country: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "myname@site.com",
                    "title": "python",
                    "salary_min": 30000,
                    "country": "arg",
                }
            ]
        }
    }
