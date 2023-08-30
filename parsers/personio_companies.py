import requests
import xml.etree.ElementTree as ET
import xmltodict
from models import jobs

ENDPOINT = "https://{company}.jobs.personio.de/xml?language=en"
JOBENDPOINT = "https://{company}.jobs.personio.de/job/{id}?display=en"
COMPANIES = ["recup", "ostrom", "gridx"]

'''
Map strings to enums
'''
def map_category(category: str) -> jobs.Category:
    if (category == "marketing_and_product"):
        return jobs.Category.MARKETING
    elif (category == "it_software"):
        return jobs.Category.ENGINEERING
    elif (category == "sales_and_business_development"):
        return jobs.Category.SALES
    elif (category == "administrative_and_clerical"):
        return jobs.Category.ADMIN
    elif (category == "production_and_operations"):
        return jobs.Category.MANUFACTURING
    elif (category == "other"):
        return jobs.Category.OTHER
    else:
        return jobs.Category.UNKNOWN

def map_seniority(seniority: str) -> jobs.Senority:
    if (seniority == "student"):
        return jobs.Senority.STUDENT
    elif (seniority == "entry-level"):
        return jobs.Senority.ENTRYLEVEL
    elif (seniority == "experienced"):
        return jobs.Senority.EXPERIENCED
    else:
        return jobs.Senority.UNKNOWN
    
def map_schedule(schedule: str) -> jobs.Schedule:
    if (schedule == "part-time"):
        return jobs.Schedule.PARTTIME
    elif (schedule == "full-time"):
        return jobs.Schedule.FULLTIME
    else:
        return jobs.Schedule.UNKNOWN
    
def map_experience(experience: str) -> jobs.Experience:
    if (experience == "lt-1"):
        return jobs.Experience.ENTRY
    elif (experience == "1-2"):
        return jobs.Experience.JUNIOR
    elif (experience == "2-5"):
        return jobs.Experience.MID
    elif (experience == "5-7"):
        return jobs.Experience.SENIOR
    else:
        return jobs.Experience.UNKNOWN

'''
Parse XML to Job Objects
'''
def get_jobs(company: str):
    company_endpoint = ENDPOINT.format(company=company)
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
            print("Request for {company} returned no positions")
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

            job = jobs.Job(
                id=position_dict['id'],
                title=position_dict['name'],
                category=job_category,
                seniority=job_seniority,
                schedule=job_schedule,
                experience=job_experience,
                link=JOBENDPOINT.format(company=company, id=position_dict['id'])
            )
            job_list.append(job)
            print("")
            print(job)

        return jobs
    
    else:
        print("Request for {company} failed with status code: {response.status_code}")
        return None

if __name__ == "__main__":
    for company in COMPANIES:
        print("----------------------")
        print(f"Fetching jobs for {company}")
        get_jobs(company)
        print("----------------------")