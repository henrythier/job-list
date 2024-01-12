from db import client
from db import models
from parsers import personio_companies

# get all companies
session = client.start_session()
company_list = client.get_all_companies(session)

# scrape all companies
for company in company_list:
    print(f"adding jobs from {company.name}")
    job_list = personio_companies.get_jobs(company)
    for job in job_list:
        job_instance = models.Job(title=job.title, category=job.category, seniority=job.seniority, experience=job.experience,
                                  schedule=job.schedule, link=job.link, company=company)
        try:
            client.add_or_update_job(job_instance, session)
        except Exception as e:
            print(e)
            print(f"could not handle: {job_instance.title}")
    print(f"added jobs from {company.name}")

client.end_session(session)
        

