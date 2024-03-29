import psycopg2
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.models import Job, Company
from dotenv import load_dotenv
import os

# Load database credentials
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# start session
def start_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def end_session(session):
    session.close()

'''
JOBS
'''
# function to update jobs
def add_or_update_job(job_instance, session):
    existing_job = session.query(Job).filter(Job.link == job_instance.link).first()

    # update
    if existing_job:
        existing_job.title = job_instance.title
        existing_job.category = job_instance.category
        existing_job.seniority = job_instance.seniority
        existing_job.experience = job_instance.experience
        existing_job.schedule = job_instance.schedule
        existing_job.link = job_instance.link
        existing_job.updated_at = func.now()

    # add
    else:
        session.add(job_instance)
    session.commit()

'''
COMPANIES
'''
# function to add companies
def add_company(link, name, jobtool):
    session = start_session()
    company_instance = Company(link, name, jobtool)
    session.add(company_instance)
    session.commit()
    end_session(session)
    print(f"Added {name} to the database")

def get_all_companies(session):
    return session.query(Company).all()

#add_company("https://recup.de/", "ReCup", "PERSONIO")