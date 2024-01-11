from db import client
from db import models
from parsers import personio_companies

# get all companies
session = client.start_session()
companies = client.get_all_companies(session)

# scrape all companies
for c in companies:
    job_list = personio_companies.get_jobs(c.name)
    for job in job_list:
        job_instance = models.Job(title=job.title, category=job.category, seniority=job.seniority, experience=job.experience,
                                  schedule=job.schedule, link=job.link, company=c)
        client.add_or_update_job(job_instance, session)
        print(f"added: {job.title} at {c.name}")

client.end_session(session)
        

