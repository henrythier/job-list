import requests

ENDPOINT = 'https://apply.workable.com/api/v3/accounts/{company}/jobs'
JOBLINK = 'https://apply.workable.com/{company}/j/{id}/'
company = 'tesseract'
    
'''
API Call
'''
headers = {
    'authority': 'apply.workable.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'content-type': 'application/json',
}

response = requests.post(
    ENDPOINT.format(company=company.lower()),
    headers=headers,
)

if response.status_code == 200:
    data = response.json()
else:
    print(f"API call failed with status code {response.status_code}")

'''
Unpack response
'''
if data["total"] > 0:
    print("loop through jobs")
    for job in data["results"]:
        link = JOBLINK.format(company=company.lower(), id=job['shortcode'])
        title = job['title']
        try:
            schedule = job['type']
        except KeyError:
            schedule = None
        job_dict = {'link': link, 'title': title, 'schedule': schedule}
        print(job_dict)
else:
    print("Workable returned no jobs.")