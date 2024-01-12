from sqlalchemy import create_engine, Column, String, DateTime, Boolean, ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from enum import Enum
from dotenv import load_dotenv
import os

# Database credentials
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()

'''
COMPANY
'''
# Company class
class Company(Base):
    __tablename__ = 'companies'

    link = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    jobtool = Column(String, nullable=False)

    # Relationship with Job class
    jobs = relationship('Job', back_populates='company')

    def __init__(self, link, name, jobtool):
        self.link = str(link)
        self.name = str(name)
        self.jobtool = str(jobtool)


'''
JOB
'''
class JobCategory(Enum):
    ADMIN = "Admin"
    ANALYTICS = "Analytics"
    ENGINEERING = "Engineering"
    MANUFACTURING = "Manufacturing"
    MARKETING = "Marketing"
    SALES = "Sales"
    OTHER = "Other"
    UNKNOWN = "Unknown"

class JobSeniority(Enum):
    STUDENT = "Student"
    ENTRYLEVEL = "Entry"
    EXPERIENCED = "Experienced"
    UNKNOWN = "Unknown"

class JobSchedule(Enum):
    FULLTIME = "Full-time"
    PARTTIME = "Part-time"
    UNKNOWN = "Unknown"

class JobExperience(Enum):
    ENTRY = "Entry"
    JUNIOR = "1-2"
    MID = "2-5"
    SENIOR = "5-7"
    UNKNOWN = "Unknown"


class Job(Base):
    __tablename__ = 'jobs'

    link = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    category = Column(SQLAlchemyEnum(JobCategory), nullable=False)
    seniority = Column(SQLAlchemyEnum(JobSeniority), nullable=False)
    experience = Column(SQLAlchemyEnum(JobExperience), nullable=False)
    schedule = Column(SQLAlchemyEnum(JobSchedule), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    live = Column(Boolean, nullable=False, default=True)
    company_link = Column(String, ForeignKey('companies.link'), nullable=False)
    company = relationship('Company', back_populates='jobs')

    def __init__(self, title, category, seniority, experience, schedule, link, company):
        self.link = str(link)
        self.title = str(title)
        self.category = JobCategory(category)
        self.seniority = JobSeniority(seniority)
        self.experience = JobExperience(experience)
        self.schedule = JobSchedule(schedule)
        self.company = company

# Create the table in the database
Base.metadata.create_all(engine)
