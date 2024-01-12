import requests
import xml.etree.ElementTree as ET
import xmltodict
from db import models

ENDPOINT = "https://{company}.jobs.personio.de/xml?language=en"
JOBENDPOINT = "https://{company}.jobs.personio.de/job/{id}?display=en"

'''
Map strings to enums
'''
def map_category(category: str) -> models.JobCategory:
    if (category == "marketing_and_product"):
        return models.JobCategory.MARKETING
    elif (category == "it_software"):
        return models.JobCategory.ENGINEERING
    elif (category == "sales_and_business_development"):
        return models.JobCategory.SALES
    elif (category == "administrative_and_clerical"):
        return models.JobCategory.ADMIN
    elif (category == "production_and_operations"):
        return models.JobCategory.MANUFACTURING
    elif (category == "other"):
        return models.JobCategory.OTHER 
    else:
        return models.JobCategory.UNKNOWN

def map_seniority(seniority: str) -> models.JobSeniority:
    if (seniority == "student"):
        return models.JobSeniority.STUDENT
    elif (seniority == "entry-level"):
        return models.JobSeniority.ENTRYLEVEL
    elif (seniority == "experienced"):
        return models.JobSeniority.EXPERIENCED
    else:
        return models.JobSeniority.UNKNOWN
    
def map_schedule(schedule: str) -> models.JobSchedule:
    if (schedule == "part-time"):
        return models.JobSchedule.PARTTIME
    elif (schedule == "full-time"):
        return models.JobSchedule.FULLTIME
    else:
        return models.JobSchedule.UNKNOWN
    
def map_experience(experience: str) -> models.JobExperience:
    if (experience == "lt-1"):
        return models.JobExperience.ENTRY
    elif (experience == "1-2"):
        return models.JobExperience.JUNIOR
    elif (experience == "2-5"):
        return models.JobExperience.MID
    elif (experience == "5-7"):
        return models.JobExperience.SENIOR
    else:
        return models.JobExperience.UNKNOWN

'''
Parse XML to Job Objects
'''
def get_jobs(company: models.Company):
    company_endpoint = ENDPOINT.format(company=company.name.lower())
    # Sending the GET request
    response = requests.get(company_endpoint)

    # Checking if the request was successful (200 OK)
    if response.status_code == 200:
        # Parsing the XML content
        xml_content = response.content
        root = ET.fromstring(xml_content)
        positions = root.findall("position")

        # Abort if no positions found
        if len(positions) == 0:
            print("Request for {company.name} returned no positions")
            return None

        # Unpack position information and drop job description
        job_list = []
        for p in positions:
            position_string = ET.tostring(p, encoding="utf-8").decode("utf-8")
            position_dict = xmltodict.parse(position_string)['position']
            position_dict.pop('jobDescriptions')

            job_category = map_category(position_dict['occupationCategory'])
            job_seniority = map_seniority(position_dict['seniority'])
            job_schedule = map_schedule(position_dict['schedule'])
            job_experience = map_experience(position_dict['yearsOfExperience'])

            job = models.Job(
                title=position_dict['name'],
                category=job_category,
                seniority=job_seniority,
                schedule=job_schedule,
                experience=job_experience,
                link=JOBENDPOINT.format(company=company.name.lower(), id=position_dict['id']),
                company=company
            )
            job_list.append(job)
        return job_list
    
    else:
        print("Request for {company.name} failed with status code: {response.status_code}")
        return None