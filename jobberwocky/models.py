from sqlalchemy import Column, Integer, String, JSON

from database import Base


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    salary = Column(Integer)
    country = Column(String, index=True)
    skills = Column(JSON)
    contact = Column(String)

    def __str__(self):
        return (
            f"Job("
            f"title='{self.title}', "
            f"salary={self.salary}, "
            f"country='{self.country}', "
            f"skills={self.skills}, "
            f"contact='{self.contact}')"
        )


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    title = Column(String)
    salary_min = Column(Integer)
    country = Column(String)

    def __str__(self):
        return (
            f"Subscription("
            f"email='{self.email}', "
            f"title='{self.title}', "
            f"salary_min={self.salary_min}, "
            f"country='{self.country}')"
        )
