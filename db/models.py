from sqlalchemy import create_engine, Column, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database credentials
DATABASE_URL = "DB URL"

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()

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

# Job class
class Job(Base):
    __tablename__ = 'jobs'

    link = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    seniority = Column(String, nullable=False)
    experience = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    live = Column(Boolean, nullable=False, default=True)
    company_link = Column(String, ForeignKey('companies.link'), nullable=False)
    company = relationship('Company', back_populates='jobs')

    def __init__(self, title, category, seniority, experience, schedule, link, company):
        self.link = str(link)
        self.title = str(title)
        self.category = str(category)
        self.seniority = str(seniority)
        self.experience = str(experience)
        self.schedule = str(schedule)
        self.company = company

# Create the table in the database
Base.metadata.create_all(engine)
